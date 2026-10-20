from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp
import os
import shutil
import tempfile

app = Flask(__name__)
DOWNLOAD_DIR = tempfile.gettempdir()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.json or {}
    url = data.get('url')
    quality = data.get('quality', '720p')

    if not url:
        return jsonify({'error': 'YouTube link din'}), 400

    cookie_path = None
    if os.path.exists('cookies.txt'):
        cookie_path = os.path.join(DOWNLOAD_DIR, 'cookies.txt')
        try:
            shutil.copy('cookies.txt', cookie_path)
        except:
            pass

    # Automatic Fallback Strategies (Ekta fail korle automatic onnote chole jabe)
    strategies = [
        {
            'format': 'best[ext=mp4]/best',
            'extractor_args': {'youtube': {'player_client': ['android']}}
        },
        {
            'format': 'b',
            'extractor_args': {'youtube': {'player_client': ['web']}}
        },
        {
            'format': 'best',
            'extractor_args': {'youtube': {'player_client': ['mweb', 'ios']}}
        }
    ]

    last_error = None
    for strat in strategies:
        ydl_opts = {
            'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title).50s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'nocheckcertificate': True,
            'format': strat['format'],
            'extractor_args': strat['extractor_args']
        }

        if cookie_path and os.path.exists(cookie_path):
            ydl_opts['cookiefile'] = cookie_path

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                return send_file(filename, as_attachment=True)
        except Exception as e:
                last_error = str(e)
                continue  # Automatic next strategy-te chole jabe

    return jsonify({'error': f'Sob method try koreodownload kora jayni: {last_error}'}), 500

app = app

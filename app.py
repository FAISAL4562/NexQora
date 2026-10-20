from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp
import os
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
        return jsonify({'error': 'ইউটিউব লিংক প্রদান করুন'}), 400

    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title).50s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'format': 'best',
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'ios', 'web']
            }
        }
    }

    if os.path.exists('cookies.txt'):
        ydl_opts['cookiefile'] = 'cookies.txt'

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': f'ডাউনলোড ব্যাহত হয়েছে: {str(e)}'}), 500

# Vercel needs this application object
app = app

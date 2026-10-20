from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp
import os
import tempfile
import static_ffmpeg

# Automatic Static FFmpeg Setup
static_ffmpeg.add_paths()

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

    # Universal Fallback Format Specs
    if quality == '1080p':
        fmt = 'bestvideo[height<=1080]+bestaudio/best[height<=1080]/b/best'
    elif quality == '720p':
        fmt = 'bestvideo[height<=720]+bestaudio/best[height<=720]/b/best'
    elif quality == '360p':
        fmt = 'bestvideo[height<=360]+bestaudio/best[height<=360]/b/best'
    elif quality == 'mp3':
        fmt = 'bestaudio/b/best'
    else:
        fmt = 'b/best'

    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title).50s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
        'concurrent_fragment_downloads': 8,
        'nocheckcertificate': True,
        'format': fmt,
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'ios', 'web']
            }
        }
    }

    if os.path.exists('cookies.txt'):
        ydl_opts['cookiefile'] = 'cookies.txt'

    if quality == 'mp3':
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            if quality == 'mp3':
                base_ext = os.path.splitext(filename)[0]
                filename = f"{base_ext}.mp3"

            return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({'error': f'ডাউনলোড ব্যাহত হয়েছে: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

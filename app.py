from flask import Flask, render_template, request, jsonify
import requests
import re

app = Flask(__name__)

def extract_video_id(url):
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed\/)([0-9A-Za-z_-]{11})',
        r'(?:watch\?v=)([0-9A-Za-z_-]{11})',
        r'(?:youtu\.be\/)([0-9A-Za-z_-]{11})'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    data = request.json or {}
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'YouTube link din'}), 400

    video_id = extract_video_id(url)
    if not video_id:
        return jsonify({'error': 'Sothik YouTube link din'}), 400

    try:
        # Piped API use kore YouTube IP block bypass korchi
        piped_url = f"https://pipedapi.kavin.rocks/streams/{video_id}"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(piped_url, headers=headers, timeout=12)
        
        if res.status_code != 200:
            return jsonify({'error': 'API theke data ana jayni, abar chesta korun'}), 500
            
        res_data = res.json()
        streams = res_data.get('videoStreams', [])
        
        if streams:
            download_url = streams[0]['url']
            return jsonify({'download_url': download_url})
        else:
            return jsonify({'error': 'Video stream pawa jayni'}), 400

    except Exception as e:
        return jsonify({'error': f'Server connection error: {str(e)}'}), 500

app = app

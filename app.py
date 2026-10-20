from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

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

    try:
        # Using a reliable alternative working API
        api_url = "https://yt-api.p.rapidapi.com/dl" # or use another public instance
        # Let's use Cobalt's new endpoint or a direct working downloader instance
        alt_api = "https://co.wuk.sh/api/json"
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0"
        }
        
        payload = {
            "url": url,
            "vQuality": quality.replace('p', ''),
            "isAudioOnly": True if quality == "mp3" else False
        }

        response = requests.post(alt_api, json=payload, headers=headers, timeout=15)
        res_data = response.json()

        if "url" in res_data:
            return jsonify({'download_url': res_data["url"]})
        elif "picker" in res_data and len(res_data["picker"]) > 0:
            return jsonify({'download_url': res_data["picker"][0]["url"]})
        else:
            return jsonify({'error': 'লিংক প্রসেস করা যায়নি, অন্য ভিডিও চেষ্টা করুন।'}), 400

    except Exception as e:
        return jsonify({'error': f'সার্ভার সংযোগে সমস্যা: {str(e)}'}), 500

app = app

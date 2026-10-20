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
        # High-Speed Public YouTube API Integration
        api_url = "https://api.cobalt.tools/api/json"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        payload = {
            "url": url,
            "vQuality": "720" if quality == "720p" else "1080" if quality == "1080p" else "360",
            "isAudioOnly": True if quality == "mp3" else False
        }

        response = requests.post(api_url, json=payload, headers=headers, timeout=10)
        res_data = response.json()

        if "url" in res_data:
            return jsonify({'download_url': res_data["url"]})
        elif "status" in res_data and res_data["status"] == "error":
            return jsonify({'error': f'API Error: {res_data.get("text", "ভিডিও প্রসেস করা যায়নি")}'}), 400
        else:
            return jsonify({'error': 'ভিডিও লিংকটি তৈরি করা সম্ভব হয়নি। আবার চেষ্টা করুন।'}), 500

    except Exception as e:
        return jsonify({'error': f'সার্ভার সংযোগে সমস্যা: {str(e)}'}), 500

app = app

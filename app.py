from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract_m3u8():
    data = request.json
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400

    try:
        response = requests.get(url)
        response.raise_for_status()

        # HTML পার্সিং
        soup = BeautifulSoup(response.text, 'html.parser')

        # m3u8 লিংক খুঁজুন
        m3u8_links = []
        for link in soup.find_all('a', href=True):
            if '.m3u8' in link['href']:
                m3u8_links.append(link['href'])

        if m3u8_links:
            return jsonify({'link': m3u8_links[0]})
        else:
            # খুঁজতে পাইনি, তবে আমরা আরও ডাইনামিক পদ্ধতি ব্যবহার করতে পারি
            video_sources = re.findall(r'src=["\'](.*?\.m3u8)["\']', response.text)
            if video_sources:
                return jsonify({'link': video_sources[0]})
        
        return jsonify({'link': None})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify, render_template
from yt_dlp import YoutubeDL

app = Flask(__name__)

def get_m3u8_link(youtube_url):
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'force_generic_extractor': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=False)
        formats = info_dict.get('formats', None)

        if formats:
            for f in formats:
                if f['ext'] == 'm3u8':
                    return f['url']
    return None

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
        m3u8_link = get_m3u8_link(url)
        if m3u8_link:
            return jsonify({'link': m3u8_link})
        else:
            return jsonify({'link': None, 'error': 'No m3u8 link found.'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

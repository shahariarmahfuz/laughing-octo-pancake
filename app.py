from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import re
from os import environ
import time

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
        # Selenium ব্যবহার করে ব্রাউজার সিমুলেট করা
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(service=ChromeService(), options=chrome_options)
        driver.get(url)
        
        # কিছু সময় অপেক্ষা করা যাতে পেজ সম্পূর্ণ লোড হয়
        time.sleep(5)

        # নেটওয়ার্ক ট্রাফিক থেকে m3u8 লিংক সংগ্রহ করার চেষ্টা করা
        m3u8_link = None
        for request in driver.requests:
            if ".m3u8" in request.url:
                m3u8_link = request.url
                break

        driver.quit()

        if m3u8_link:
            return jsonify({'link': m3u8_link})
        else:
            return jsonify({'link': None})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(environ.get('PORT', 5000)), debug=True)

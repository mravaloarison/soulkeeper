
from flask import jsonify
import os, requests

NEWS_API_KEY = os.environ.get("NEWS_API_KEY")
NEWS_API_BASE_URL = 'https://newsapi.org/v2/'

categories = [
    { "name": "general", "emoji": "🤷‍♂️" },
    { "name": "business", "emoji": "🤝" },
    { "name": "entertainment", "emoji": "🎬" },
    { "name": "health", "emoji": "🩺" },
    { "name": "science", "emoji": "🧬" },
    { "name": "sports", "emoji": "🏅" },
    { "name": "technology", "emoji": "👨‍💻" }
]

def make_news_api_request(endpoint, params={}):
    url = f'{NEWS_API_BASE_URL}{endpoint}?apiKey={NEWS_API_KEY}'
    url += ''.join([f'&{k}={v}' for k, v in params.items()])
    response = requests.get(url)
    return jsonify(response.json()) if response.status_code == 200 else jsonify({'error': 'Failed to fetch news'})
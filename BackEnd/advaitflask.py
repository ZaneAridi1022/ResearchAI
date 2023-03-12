import asyncio
from flask import Flask, request, abort
from recommend import Recommendation
import socket

app = Flask(__name__)


def validate_url(url):
    if not url.endswith('.pdf'):
        abort(400, "URL must end with '.pdf'")


@app.route('/')
def index():
    return {'message': 'Hello World'}


@app.route('/summary', methods=['GET'])
def summarize():
    url = request.json['url']
    validate_url(url)
    summary = Recommendation().summarize_text(url)
    return {'summary': summary}


@app.route('/support', methods=['GET'])
def support():
    mode = 'support'
    url = request.json['url']
    validate_url(url)
    urls = asyncio.run(Recommendation().action(mode, url))
    return {'urls': urls}


@app.route('/refute', methods=['GET'])
def refute():
    mode = 'refute'
    url = request.json['url']
    validate_url(url)
    urls = asyncio.run(Recommendation().action(mode, url))
    return {'urls': urls}


@app.route('/recommend', methods=['GET'])
def recommend():
    prompt = request.json['prompt']
    urls = asyncio.run(Recommendation().recommend(prompt))
    return {'urls': urls}


if __name__ == '__main__':
    socket.setdefaulttimeout(60)
    app.run(debug=True)

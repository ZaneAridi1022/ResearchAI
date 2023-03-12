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
    url = request.args.get('url')
    validate_url(url)
    summary = Recommendation().summarize_text(url)
    return {'summary': summary}


@app.route('/recommend', methods=['GET'])
def recommend():
    prompt = request.args.get("prompt")
    if not prompt:
        abort(400, "Missing prompt")
    if ".pdf" in prompt:
        validate_url(prompt)
        prompt = Recommendation().summarize_text(prompt)
    json_ = asyncio.run(Recommendation().recommend(prompt))
    return json_

if __name__ == '__main__':
    socket.setdefaulttimeout(60)
    app.run(debug=True)
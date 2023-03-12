# from chatgpt import generate
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/")
def stratHere():
    return "Hello World!"

@app.route("/evaluate")
def evaluate_query():
    prompt = request.args.get("prompt")
    response = jsonify({"test":prompt})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
    while True:
        prmpt = input("Enter prompt")
        if prmpt == "E":
            break
        print(generate(prmpt))

if __name__ == "__main__":
    app.run(debug=True)
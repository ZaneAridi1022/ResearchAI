from chatgpt import generate
from flask import Flask, jsonify, request


app = Flask(__name__)
# import edge
# import scholarscraper

class EvaluteResponse(object):
    def __init__(self, query: str, support: list, refuations: list):
        self.query = query
        self.support = support
        self.refutations = refuations

class Study(object):
    def __init__(self, argument: str, studyName: str, studySummary: str, sourceUrl: str, strengths: str, limitations: str):
        self.argument = argument
        self.studyName = studyName
        self.studySummary = studySummary
        self.sourceUrl = sourceUrl
        self.strengths = strengths
        self.limitations = limitations

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
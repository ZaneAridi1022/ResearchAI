from chatgpt import generate
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

while True:
    prmpt = input("Enter prompt")
    if prmpt == "E":
        break
    print(generate(prmpt))
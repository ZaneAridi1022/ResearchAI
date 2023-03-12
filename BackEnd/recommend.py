import json
import os
import re
import io
import asyncio
import requests
from dotenv import load_dotenv
import PyPDF2
import openai
import cohere
from EdgeGPT import Chatbot, ConversationStyle

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')


class Recommendation:
    def __init__(self):
        self.co = cohere.Client(os.getenv('COHERE_API'))
        self.bot = Chatbot(cookiePath='backend/cookies.json')
        
    @staticmethod
    def convert_pdf_to_string(url):
        r = requests.get(url)
        f = io.BytesIO(r.content)
        reader = PyPDF2.PdfReader(f)
        content = ""
        for page in reader.pages:
            content += page.extract_text()
        return content

    def summarize_text(self, url):
        text = self.convert_pdf_to_string(url)
        response = self.co.summarize(
            text=text,
            model='summarize-xlarge',
            length='long',
            format='paragraph',
            extractiveness='medium',
            temperature=0.5,
            additional_command="in third person pov"
        )
        return response.summary

    @staticmethod
    def extract_url(text):
        urls = re.findall(r'(https?://\S+)', text) if ")" not in text else re.findall(r'(https?://\S+)',
                                                                                      text.split(")")[1])
        return urls

    def generate(self, topic):
        json_format = """
        {
            "topic": "topic",
            "supporting_arguments": [
                {
                "tagline": "tagline",
                "argument": "argument"
                }
            ],
            "refuting_arguments": [
                {
                "tagline": "tagline",
                "argument": "argument"
                }
            ]
        }
        """
        prompt = f"Please provide supporting and refuting arguments for {topic} in one dictionary JSON format like so {json_format}.  Please include short taglines for each argument that succinctly capture its main point."
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt},
            ]
        )
        return self.text_to_json(response["choices"][0]["message"]["content"])

    @staticmethod
    def text_to_json(json_string):
        while "\n" in json_string:
            json_string = json_string.replace("\n", '')
        while "  " in json_string:
            json_string = json_string.replace("  ", ' ')
        match = re.search("({.*})", json_string)
        try:
            json_ = eval(match.group(1))
        except:
            json_ = json.loads(match.group(1))
        return json_

    @staticmethod
    def get_all_urls(response):
        sources = response["item"]['messages'][1]['sourceAttributions']
        all_urls = []
        for source in sources:
            all_urls.append(source["seeMoreUrl"])
        all_urls = list(set(all_urls))
        return all_urls

    async def get_json(self, topic):
        json_found = False
        while not json_found:
            try:
                json_ = self.generate(topic)
                json_found = True
                print(json_)
            except:
                continue
        return json_

    async def process_argument(self, argument, semaphore):
        async with semaphore:
            bot = Chatbot(cookiePath='backend/cookies.json')
            print(argument['argument'])
            response = await bot.ask(prompt=f"Act as a researcher. Provide academic papers in PDF format for this {argument['argument']}",
                                    conversation_style=ConversationStyle.creative)
            print(response)
            argument["urls"] = self.get_all_urls(response)
            await bot.close()

    async def process_arguments(self, arguments, semaphore):
        tasks = []
        for argument in arguments:
            task = asyncio.ensure_future(self.process_argument(argument, semaphore))
            tasks.append(task)
        await asyncio.gather(*tasks)

    async def recommend(self, topic):
        json_ = await self.get_json(topic)

        semaphore = asyncio.Semaphore(50)

        await self.process_arguments(json_["supporting_arguments"], semaphore)
        await self.process_arguments(json_["refuting_arguments"], semaphore)
        print(json_)
        return json_

    


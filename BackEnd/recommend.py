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
        self.semaphore = asyncio.Semaphore(5)
        
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
        json_format = "{'topic':topic, 'supporting_arguments':[{'tagline':tagline, 'argument':argument}], 'refuting_arguments':[{'tagline':tagline, 'argument':argument}]}"
        prompt = f"Please provide supporting and refuting arguments for {topic} in one dictionary JSON format like so {json_format}.  Please include short taglines for each argument that succinctly capture its main point."
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt},
            ]
        )
        print(response["choices"][0]["message"]["content"])
        return self.text_to_json(response["choices"][0]["message"]["content"])

    @staticmethod
    def text_to_json(json_string):
        while "\n" in json_string:
            json_string = json_string.replace("\n", '')
        while "  " in json_string:
            json_string = json_string.replace("  ", ' ')
        match = re.search("({.*})", json_string)
        return eval(match.group(1))

    @staticmethod
    def get_all_urls(response):
        sources = response["item"]['messages'][1]['sourceAttributions']
        all_urls = []
        for source in sources:
            all_urls.append(source["seeMoreUrl"])
        all_urls = list(set(all_urls))
        return all_urls


    async def fetch_urls(self, semaphore, argument):
        async with semaphore:
            response = await self.bot.ask(prompt=f"Act as a researcher. Provide scholarly articles for this {argument['argument']}",
                                    conversation_style=ConversationStyle.creative)
            print(response)
            argument["urls"] = self.get_all_urls(response)

    async def recommend(self, topic):
        json_ = self.generate(topic)
        
        # create a Semaphore with maximum value of 2
        semaphore = asyncio.Semaphore(2)
        
        supporting_tasks = [asyncio.create_task(self.fetch_urls(semaphore, argument)) for argument in json_["supporting_arguments"]]
        refuting_tasks = [asyncio.create_task(self.fetch_urls(semaphore, argument)) for argument in json_["refuting_arguments"]]
        
        # wait for all tasks to complete
        await asyncio.gather(*supporting_tasks, *refuting_tasks)
        
        await self.bot.close()
        return json_


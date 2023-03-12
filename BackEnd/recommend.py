import os
import re
import io

import asyncio
import requests
from dotenv import load_dotenv
import PyPDF2
from EdgeGPT import Chatbot, ConversationStyle
import cohere

load_dotenv()


class Recommendation:
    def __init__(self):
        self.co = cohere.Client(os.getenv('COHERE_API'))
        self.bot = Chatbot(cookiePath='cookies.json')

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
    @staticmethod
    def get_all_urls(response):
        sources = response["item"]['messages'][1]['sourceAttributions']
        print(sources)
        all_urls = []
        for source in sources:
            all_urls.append(source["seeMoreUrl"])
        all_urls = list(set(all_urls))
        return all_urls

    async def recommend(self, prompt):
        response = await self.bot.ask(prompt=f"Recommend a few scholarly articles that talk about {prompt}",
                                      conversation_style=ConversationStyle.creative)
        return self.get_all_urls(response)

    async def action(self, mode, article):
        response = await self.bot.ask(prompt=f"Act as a researcher. Provide arguments that {mode} this {article}",
                                      conversation_style=ConversationStyle.creative)
        return self.get_all_urls(response)

    async def close(self):
        await self.bot.close()


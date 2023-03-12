import asyncio
from EdgeGPT import Chatbot, ConversationStyle
import re

async def recommend(prompt):
    bot = Chatbot(cookiePath='backend/cookies.json')
    response = await bot.ask(prompt=f"Recommend me research papers that talk about {prompt}", conversation_style=ConversationStyle.creative)
    await bot.close()
    return response

def extract_url(text):
    urls = re.findall(r'(https?://\S+)', text) if ")" not in text else re.findall(r'(https?://\S+)', text.split(")")[1])
    return urls

def get_all_urls(response):
    sources = response["item"]["messages"][1]['adaptiveCards'][0]['body']
    all_urls = []
    for source in sources:
        all_urls += extract_url(source['text'])
    all_urls = list(set(all_urls))
    return all_urls
async def action(mode, article):
    bot = Chatbot(cookiePath='backend/cookies.json')
    response = await bot.ask(prompt=f"Act as a researched. Provide argments that {mode} this {article}", conversation_style=ConversationStyle.creative)
    await bot.close()
    return get_all_urls(response)

if __name__ == "__main__":
    pass
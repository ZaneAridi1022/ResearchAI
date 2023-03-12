import asyncio
from EdgeGPT import Chatbot, ConversationStyle

async def process_bot_request(semaphore):
    async with semaphore:
        bot = Chatbot(cookiePath='backend/cookies.json')
        print(await bot.ask(prompt="Hello world", conversation_style=ConversationStyle.creative))
        await bot.close()

async def main():
    semaphore = asyncio.Semaphore(100)

    tasks = []

    for i in range(10):
        tasks.append(asyncio.ensure_future(process_bot_request(semaphore)))

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())

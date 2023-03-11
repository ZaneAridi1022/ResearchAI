import asyncio
from EdgeGPT import Chatbot, ConversationStyle

async def main():
    bot = Chatbot()
    print(await bot.ask(prompt="Hello world", conversation_style=ConversationStyle.creative))
    await bot.close()


if __name__ == "__main__":
    asyncio.run(main())

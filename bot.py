import openai
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from aiogram import F
from decouple import config


openai.api_key = config("API_KEY")
bot = Bot(token=config("BOT_TOKEN"))
dp = Dispatcher()


@dp.message(Command("start"))
async def send_welcome(message: types.Message):
    await message.answer(
        "Привет! Отправь мне новость, и я сгенерирую забавный комментарий для неё."
    )


@dp.message(F.text)
async def process_news(message: types.Message):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a social network user who wants to leave a short funny comment under the news. Comment in one short sentence.",
            },
            {"role": "user", "content": message.text},
        ],
    )

    comment = completion.choices[0].message.content

    await message.answer(comment)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

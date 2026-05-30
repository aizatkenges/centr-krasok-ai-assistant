import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.enums import ChatAction
from dotenv import load_dotenv

from ai_service import ask_ai

load_dotenv()

logging.basicConfig(level=logging.INFO)

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

user_history = {}


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "👋 Здравствуйте! Я AI-Консультант Центр Красок #1.\n\n"
        "Могу помочь с:\n"
        "• подбором материалов;\n"
        "• информацией о продукции\n"
        "• услугами компании;\n"
        "• контактами;\n"
        "• сотрудничеством.\n\n"
        "Какой вопрос вас интересует?"
    )


@dp.message()
async def chat(message: Message):
    user_id = message.from_user.id
    user_text = message.text

    if not user_text:
        await message.answer("Пожалуйста, напишите вопрос текстом.")
        return

    if user_id not in user_history:
        user_history[user_id] = []

    await bot.send_chat_action(
        chat_id=message.chat.id,
        action=ChatAction.TYPING
    )
    text = user_text.lower().strip()

    if text in ["привет", "здравствуйте", "добрый день", "добрый вечер"]:
        await message.answer(
        "Здравствуйте! 👋 Я AI-консультант Центр Красок #1. Могу помочь с вопросами о продукции, услугах, контактах и сотрудничестве. Чем могу помочь?"
    )
        return

    if text in ["спасибо", "благодарю", "thanks", "thank you"]:
        await message.answer(
            "Рад был помочь! 😊 Если появятся дополнительные вопросы о продукции или услугах компании, обращайтесь."
    )
        return

    if text in ["пока", "до свидания", "всего доброго"]:
        await message.answer(
            "Спасибо за обращение в Центр Красок #1! Хорошего дня! 👋"
    )
        return
    try:
        
        answer = ask_ai(user_text, user_history[user_id])

        user_history[user_id].append({
            "role": "user",
            "content": user_text
        })

        user_history[user_id].append({
            "role": "assistant",
            "content": answer
        })

        await message.answer(answer)

    except Exception as error:
        logging.exception("AI error")
        await message.answer(
            "Извините, сейчас не получилось обработать запрос. "
            "Попробуйте ещё раз чуть позже."
        )


async def main():
    logging.info("Bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
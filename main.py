from aiogram import Bot
import asyncio

bot = Bot(token="7130020796:AAHjYgrO1PevetGReQVvdTGBralfm93jax4")

async def send_message(chat_id, text):
    await bot.send_message(chat_id=chat_id, text=text)

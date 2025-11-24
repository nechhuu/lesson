import asyncio
import httpx
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.types import BotCommand, ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv

import os

load_dotenv()


BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


@dp.message(Command("menu"))
async def menu(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Фото"), KeyboardButton(text="Сообщение")]],
        resize_keyboard=True,
    )

    await message.answer("Выберите действие", reply_markup=keyboard)


async def set_commands():
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Начать бота"),
            BotCommand(command="help", description="Помощь бота"),
            BotCommand(command="menu", description="Меню"),
            BotCommand(command="currency", description="Валюты"),
        ],
    )


@dp.message(Command("help"))
async def help_command(message: Message):
    help_text = (
        "/start — старт команда\n"
        "/photo — обработчик фоток\n"
        "/text — обработчик текста"
    )
    await message.reply(help_text)


@dp.message(F.photo)
async def photo_command(message: Message):
    await message.reply("Классная фотка")


@dp.message(CommandStart())
async def start_command(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Факт о кошках")]],
        resize_keyboard=True,
    )
    await message.answer(text="choose", reply_markup=keyboard)


@dp.message(Command("currency"))
async def currency_command(message: Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="KGS"),
                KeyboardButton(text="EUR"),
                KeyboardButton(text="ZAR"),
            ]
        ],
        resize_keyboard=True,
    )
    await message.answer("Выбери валюту", reply_markup=keyboard)


@dp.message(F.text == "KGS")
async def currency_kgc(message: Message):
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.exchangerate-api.com/v4/latest/USD")
        rates = response.json()["rates"]["KGS"]
    await message.answer(f"Текущий курс KGS к USD: {rates}")


@dp.message(F.text == "EUR")
async def currency_eur(message: Message):
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.exchangerate-api.com/v4/latest/USD")
        rates = response.json()["rates"]["EUR"]
    await message.answer(f"Текущий курс EUR к USD: {rates}")


@dp.message(F.text == "ZAR")
async def currency_zar(message: Message):
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.exchangerate-api.com/v4/latest/USD")
        rates = response.json()["rates"]["ZAR"]
    await message.answer(f"Текущий курс ZAR к USD: {rates}")


@dp.message(F.text == "Факт о кошках")
async def facts(message: Message):
    async with httpx.AsyncClient() as client:
        response = await client.get("https://catfact.ninja/fact")
        fact = response.json()["fact"]
    await message.answer(fact)


async def main():
    await set_commands()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

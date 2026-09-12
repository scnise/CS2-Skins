import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

BOT_TOKEN = "8647898726:AAHEuF_PWXCLI_HV5IhC4hPjc8p8q-ANDlY"
WEB_APP_URL = "http://localhost:8080/"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def on_startup():
    print("---------------------------------")
    print("Бот успешно запущен и готов к работе!")
    print("---------------------------------")

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Открыть приложение",
                    web_app=WebAppInfo(url=WEB_APP_URL)
                )
            ]
        ]
    )
    await message.answer("Привет! Нажми кнопку ниже, чтобы открыть приложение:", reply_markup=keyboard)

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

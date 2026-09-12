import asyncio
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

BOT_TOKEN = "8647898726:AAF-f2Rg8IZyxj2-DMn00fBqLsSMsy3xN-c"
WEB_APP_URL = "https://734d3f6786beaf.lhr.life"  # Будет открываться в Telegram на этом ПК

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Находим путь к папке frontend с файлом index.html
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend"))

# Обработчик, который отдает твой index.html браузеру / телеграму
async def serve_index(request):
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return web.FileResponse(index_path)
    return web.Response(text="Файл frontend/index.html не найден!", status=404)

# Обработчик команды /start в боте
@dp.message(CommandStart())
async def start_handler(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Открыть CS2-Skins 🎮",
                    web_app=WebAppInfo(url=WEB_APP_URL)
                )
            ]
        ]
    )
    await message.answer("Привет! Нажми на кнопку ниже, чтобы открыть витрину скинов:", reply_markup=keyboard)

# Главная функция: запускает одновременно и сервер макета, и бота
async def main():
    # 1. Запускаем локальный веб-сервер на 8080 порту
    app = web.Application()
    app.router.add_get("/", serve_index)
    
    # Если во frontend есть картинки, css или js — раздаем их тоже
    if os.path.exists(FRONTEND_DIR):
        app.router.add_static("/static/", path=FRONTEND_DIR, name="static")

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "localhost", 8080)
    await site.start()
    print("-----------------------------------------")
    print(" Веб-сервер запущен: http://localhost:8080")
    print(" Бот успешно запущен и готов к работе!")
    print("-----------------------------------------")

    # 2. Запускаем опрос сообщений Telegram
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
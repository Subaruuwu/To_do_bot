import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from bot.configuration import TgKeys
from bot.handlers import register_all_handlers


async def __on_start_up(dp: Dispatcher) -> None:
    print('registration handlers')
    register_all_handlers(dp)


async def start_bot():
    bot = Bot(token=TgKeys.TOKEN, parse_mode='HTML')
    dp = Dispatcher()
    print('system message: bot is started')
    await __on_start_up(dp)
    await dp.start_polling(bot)

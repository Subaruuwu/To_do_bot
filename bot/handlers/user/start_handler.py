from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove

# todo: имопорт клавиатуры
# todo: импорт текста и данных

router = Router()


@router.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer('Добро пожаловать в бота!')

@router.message(F.text)
async def answer(message: Message):
    await message.answer('Инструкция')

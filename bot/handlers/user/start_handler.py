from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from bot.data.data_message import DataDict
from bot.keyboards import main_choser


# todo: имопорт клавиатуры
# todo: импорт текста и данных

router = Router()


@router.message(Command('start'))
async def cmd_start(message: Message):
    message_answer = DataDict.DATAMESSAGE["start"]
    for one_message in message_answer[:-1]:
        await message.answer(one_message)
    await message.answer(message_answer[-1], reply_markup=main_choser())


@router.message(F.text.lower() == "инструкция")
@router.message(Command('help'))
async def answer(message: Message):
    await message.answer('Инструкция, Даша представь что тут много букав')

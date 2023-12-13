from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from bot.data.data_message import DataDict


def main_choser() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    button_list = DataDict.DATAMESSAGE["main_choser"]
    for button in button_list:
        kb.button(text=button)
    kb.adjust(3)
    return kb.as_markup(resize_keyboard=True)

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def make_yes_no_keyboard() -> ReplyKeyboardMarkup:
    items = ['Да', 'Нет']
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)
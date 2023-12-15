from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def make_numbers_of_tasks_keyboard(list_of_number_tasks) -> ReplyKeyboardMarkup:
    items = list_of_number_tasks
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)

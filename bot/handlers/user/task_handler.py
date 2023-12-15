from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from bot.data.data_message import DataDict
from bot.keyboards import main_choser
from bot.keyboards import make_yes_no_keyboard

from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from bot.data import take_list_of_tasks
from bot.keyboards import make_numbers_of_tasks_keyboard

router = Router()

# todo: Добавить класс со стейтами

#Посмотреть доступные задачи
@router.message(F.text.lower() == 'посмотреть задачи')
async def watch_all_tasks(message: Message, state = FSMContext):
    list_of_tasks = take_list_of_tasks(message.from_user.id)
    head = 'Список ваших задач:\n'
    data_message = ['Номер задания: {} Задание: {} Время на выполнение: {}'.format(str(index+1), task[0], task[1]) for index, task in enumerate(list_of_tasks)]
    data = '\n'.join(data_message)
    data_message = head + data
    list_of_numbers = [str(index+1) for index in range(len(list_of_tasks))]
    keyboard = make_numbers_of_tasks_keyboard(list_of_numbers)
    await message.answer(data_message, reply_markup=keyboard)

    pass
    # todo: Получить список дел из модуля из data
    # todo: Получить список кнопок из модуля из keyboards
    # todo: Связать задачи с кнопками
    # todo: Вывести всё на экран и установить стейт


'''
#Посмотреть выполненные задачи
# todo: написать функцию, использовать получение сводки из data.data_functions

@router.message(pass)
async def chose_way_for_task(message: Message, state = FSMContext):
    pass
    # todo: Вывести список кнопок из keyboards с выбором   Удалить задачу или приступить к выполнению задачи



# todo: приступить к выполнению задачи
# todo: импортировать зачу из data_funcctions write_tasks_to_active_tasks_csv
@router.message(pass)
async def finish_active_task(message: Message, state = FSMContext):
    pass
    # todo: получить активную задачу из файла с активными задачами
    # todo: Завершить её выполнение
    # todo: Удалить задачу из списка активных задач
    # todo: Переместить задчу в выполненные задачи
    # todo: Показать награду и сводку времени


@router.message(pass)
async def delete_task(message: Message, state = FSMContext):
    pass
    # todo: удалить задачу

'''
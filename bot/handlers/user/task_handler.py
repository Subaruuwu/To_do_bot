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
from bot.keyboards import make_numbers_of_tasks_keyboard, make_yes_no_keyboard_for_doing_task
from bot.data import write_tasks_to_active_tasks_csv

router = Router()


class TaskHandlerStates(StatesGroup):
    waiting_for_choosing_task = State()
    waiting_for_time_response = State()
    begin_doing_task = State()
# todo: Добавить класс со стейтами

#Посмотреть доступные задачи
@router.message(F.text.lower() == 'посмотреть задачи')
async def watch_all_tasks(message: Message, state: FSMContext):
    list_of_tasks = take_list_of_tasks(message.from_user.id)
    head = 'Список ваших задач:\n'
    data_message = ['Номер задания: {} Задание: {} Время на выполнение: {}'.format(str(index+1), task[0], task[1]) for index, task in enumerate(list_of_tasks)]
    data = '\n'.join(data_message)
    data_message = head + data
    list_of_numbers = [str(index+1) for index in range(len(list_of_tasks))]
    keyboard = make_numbers_of_tasks_keyboard(list_of_numbers)
    await message.answer(data_message, reply_markup=keyboard)
    dict_of_tasks = dict(zip(list_of_numbers, list_of_tasks))
    print(dict_of_tasks)
    await state.set_state(TaskHandlerStates.waiting_for_choosing_task)
    await state.update_data(dict_of_tasks=dict_of_tasks)


#Посмотреть выполненные задачи
# todo: написать функцию, использовать получение сводки из data.data_functions

@router.message(TaskHandlerStates.waiting_for_choosing_task)
async def chose_way_for_task(message: Message, state: FSMContext):
    data_message = await state.get_data()
    number_of_tasks = data_message['dict_of_tasks'].keys()
    dict_of_tasks = data_message['dict_of_tasks']
    print(number_of_tasks)
    number_of_selected_task = message.text.lower()
    if number_of_selected_task in number_of_tasks:
        head = 'Вы выбрали задание:\n'
        task_data = dict_of_tasks[number_of_selected_task]
        data_message_body = 'Номер задания: {} \nЗадание: {} \nВремя на выполнение: {}\n'.format(str(number_of_selected_task), task_data[0], task_data[1])
        tail = 'Всё правильно?'
        message_text = head + data_message_body + tail
        await state.set_state(TaskHandlerStates.begin_doing_task)
        await state.update_data(number_of_selected_task=number_of_selected_task)
        await state.update_data(task_data=task_data)
        await message.answer(message_text, reply_markup=make_yes_no_keyboard_for_doing_task())
    else:
        await message.answer('Проверьте правильность ввода номера задания')
        print('выведено сообжение о несоответствии')
        await state.clear()
        print('очищен стейт')
        await watch_all_tasks(message, state)
    # todo: Вывести список кнопок из keyboards с выбором   Удалить задачу или приступить к выполнению задачи

'''
@router.message(TaskHandlerStates.begin_doing_task, F.text.in_(['Да, начать выполнение', 'Нет']))
async def watch_all_tasks(message: Message, state: FSMContext):
    choose_of_user = message.text.lower()
    if choose_of_user == 'да, начать выполнение':
        data_message = await state.get_data()
        number_of_selected_task = data_message['number_of_selected_task']
        task_data = data_message['task_data']
        write_tasks_to_active_tasks_csv(str(message.from_user.id), task_data[0], task_data[1])
        await message.answer('Вы успешно начали выполнение задания!')
        # todo: сделать запись в active task
    elif choose_of_user == 'нет':
        # todo: вернуться в главнй стейт
        pass
'''

'''
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
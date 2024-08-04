from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from bot.data.data_message import DataDict
from bot.keyboards import main_choser
from bot.keyboards import make_yes_no_keyboard, make_yes_no_keyboard_for_doing_task

from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from bot.data import write_tasks_to_list_of_tasks_csv
from bot.data import write_tasks_to_active_tasks_csv


router = Router()


class TaskMakerStates(StatesGroup):
    waiting_for_task_description = State()
    waiting_for_time_response = State()
    waiting_for_verification = State()
    begin_doing_task = State()


@router.message(F.text.lower() == "создать задачу")
async def task_maker(message: Message, state: FSMContext):
    message_answer = DataDict.DATAMESSAGE["make_task"]
    await message.answer(message_answer[0])
    await state.set_state(TaskMakerStates.waiting_for_task_description)
    await state.update_data(message_answers=message_answer)

# todo: обавить отработку неправильного вывода


@router.message(TaskMakerStates.waiting_for_task_description)
async def choosing_time_for_task(message: Message, state: FSMContext):
    await state.update_data(task_name=message.text.lower())
    message_answer = await state.get_data()
    await message.answer(text=message_answer["message_answers"][1])
    await state.set_state(TaskMakerStates.waiting_for_time_response)


# todo: обавить отработку неправильного вывода


@router.message(TaskMakerStates.waiting_for_time_response)
async def checking_task_is_correct(message: Message, state: FSMContext):
    await state.update_data(task_time=message.text.lower())
    message_answer = await state.get_data()
    await message.answer(message_answer["message_answers"][2].format(message_answer['task_name'],
                                                                     message_answer['task_time']),
                         reply_markup=make_yes_no_keyboard())
    await state.set_state(TaskMakerStates.waiting_for_verification)


@router.message(TaskMakerStates.waiting_for_verification, F.text.in_(['Да', 'Нет']))
async def task_verification(message: Message, state: FSMContext):
    message_answer = await state.get_data()
    if message.text.lower() == 'да':
        user_data = [message.from_user.id, message_answer['task_name'], message_answer['task_time']]
        write_tasks_to_list_of_tasks_csv(user_data)
        await state.set_state(TaskMakerStates.begin_doing_task)
        await message.answer(message_answer["message_answers"][3], reply_markup=make_yes_no_keyboard_for_doing_task())  # todo: add reply markup keyboard
    elif message.text.lower() == 'нет':
        await message.answer('Сочувствуем:(')
        # await state.set_state(TaskMakerStates.waiting_for_time_response)
        await state.clear()


@router.message(TaskMakerStates.begin_doing_task, F.text.in_(['Да, начать выполнение', 'Нет']))
async def begin_doing_task(message: Message, state: FSMContext):
    choose_of_user = message.text.lower()
    if choose_of_user == 'да, начать выполнение':
        data_message = await state.get_data()
        # number_of_selected_task = data_message['number_of_selected_task']
        # task_data = data_message['task_data']
        # write_tasks_to_active_tasks_csv(str(message.from_user.id), task_data[0], task_data[1])
        await message.answer('Вы успешно начали выполнение задания!')
        # todo: сделать запись в active task
    elif choose_of_user == 'нет':
        # todo: вернуться в главнй стейт
        await state.clear()
        await message.answer('Вы отменили выбор задания')
        await message.answer('Главное меню', reply_markup=main_choser())
        pass
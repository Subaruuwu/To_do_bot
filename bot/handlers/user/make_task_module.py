from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from bot.data.data_message import DataDict
from bot.keyboards import main_choser
from bot.keyboards import make_yes_no_keyboard

from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from bot.data import write_tasks_to_list_of_tasks_csv


router = Router()


class TaskMakerStates(StatesGroup):
    waiting_for_task_description = State()
    waiting_for_time_response = State()
    waiting_for_verification = State()


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
async def choosing_time_for_task(message: Message, state: FSMContext):
    message_answer = await state.get_data()
    if message.text.lower() == 'да':
        user_data = [message.from_user.id, message_answer['task_name'], message_answer['task_time']]
        write_tasks_to_list_of_tasks_csv(user_data)
        await message.answer(message_answer["message_answers"][3])
    elif message.text.lower() == 'нет':
        await message.answer('Сочувствуем:(')
    await state.set_state(TaskMakerStates.waiting_for_time_response)
    await state.clear()
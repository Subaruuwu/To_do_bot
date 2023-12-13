from aiogram import Dispatcher
from bot.handlers.user.start_handler import router as start_router
from bot.handlers.user.make_task_module import router as task_maker

# todo: Написать другие хендлеры


def register_user_handlers(dp: Dispatcher):
    # todo: register all user handlers
    list_of_routers = [start_router, task_maker]
    for router in list_of_routers:
        dp.include_router(router)
    print('Проведена регистрация хендлеров пользователя')

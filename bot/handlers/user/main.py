from aiogram import Dispatcher
from bot.handlers.user.start_handler import router as start_router

# todo: Написать другие хендлеры


def register_user_handlers(dp: Dispatcher):
    # todo: register all user handlers
    list_of_routers = [start_router]
    for router in list_of_routers:
        dp.include_router(router)
    print('Проведена регистрация хендлеров пользователя')

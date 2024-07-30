from aiogram.dispatcher.filters.state import State, StatesGroup


class user_info(StatesGroup):
    name = State()
    age = State()

    photo = State()
    city = State()


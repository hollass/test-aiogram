import asyncio
from datetime import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType

from info.config import api_key, NOTIFICATION_TIME
from info.fsm import user_info
from info.keyboards.inline import keys
from logic.api import weather

from main import dp, mes, bot
from database.db import users

from PIL import Image


# Database
us = users()
# keyboards
keyboard = keys()

# FSM
fsm = user_info()

# api
weat = weather(api_key)

@dp.message_handler(commands='help')
async def admins(mes: mes):
    commands = ['/start', '/help', '/echo', '/photo', '/keys', '/name', '/weather', '/users']
    await mes.answer(f'Список доступных команд:\n\n'
                     f'{", ".join(commands)}')

@dp.message_handler(commands='keys')
async def view_keys(mes: mes):
    await mes.answer('Просмотр клавиатуры: ', reply_markup=await keyboard.test_key())


@dp.message_handler(commands='weather')
async def view_keys(mes: mes):
    await mes.answer('Введите город')
    await fsm.city.set()

@dp.message_handler(commands='name')
async def info_name(mes: mes):
    await mes.answer('Введите ваше имя')
    await fsm.name.set()
@dp.message_handler(state=fsm.city)
async def save_name(mes: mes, state: FSMContext):
    try:
        await mes.answer(weat.get(mes.text))
    except:
        await mes.answer('Не удалось получить данные о погоде')
    await state.finish()

@dp.message_handler(state=fsm.name)
async def save_name(mes: mes, state: FSMContext):
    await state.update_data(name=mes.text)
    await mes.answer(f'Привет, {mes.text}!\n'
                     f'Теперь введи свой возраст!')

    await fsm.age.set()


@dp.message_handler(state=[fsm.age,fsm.name])
async def save_age(mes: mes, state: FSMContext):
    try:
        int(mes.text)
        await state.update_data(age=mes.text)

        data = await state.get_data()
        await mes.answer(f'Привет, {data["name"]}!\n'
                         f'Твой возраст: {data["age"]}')

        await us.add_user(mes.from_user.id, data['name'], mes.text)
        await state.finish()
    except ValueError:
        await mes.answer('Ввели не число! Начать сначала - /name')
        await state.finish()


@dp.message_handler(commands='users')
async def get_users(mes: mes):
    users_list = await us.get_users()

    await mes.answer(f'Список пользователей:\n\n'
                     f'{", ".join([f"{user[0]}" for user in users_list])}')


@dp.message_handler(commands='photo')
async def add_photo(mes: mes):
    await mes.answer('Отправьте фотографию')


@dp.message_handler(content_types=ContentType.PHOTO)
async def save_photo(mes: mes, state: FSMContext):
    await mes.photo[-1].download('photo/test.jpg')

    with Image.open('photo/test.jpg') as image:
        width, height = image.size
    await mes.answer(f'Ширина фото - {width}\n'
                     f'Высота фото - {height}')






@dp.message_handler(commands='echo')
async def echo(mes: mes):
    await mes.answer(f'Привет, {mes.from_user.full_name}!\n'
                     f'Введи любой текст.')

@dp.message_handler()
async def echo_text(mes: mes):
    await mes.reply(mes.text)


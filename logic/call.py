from aiogram import types
from aiogram.dispatcher import FSMContext

from info.keyboards.inline import keys

from main import dp

keyboard = keys()


@dp.callback_query_handler(text=['one', 'two'])
async def on_callback(call: types.CallbackQuery, state: FSMContext):
    words = {'one': 'Выбор 1', 'two': 'Выбор 2'}
    print(call.data)

    await call.message.answer(words[call.data], reply_markup=await keyboard.test_key())

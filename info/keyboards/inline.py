from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class keys():
    async def test_key(self):
        maps = InlineKeyboardMarkup(one_time_keyboard=True, row_width=2)
        for i in [['Выбор 1','one'], ['Выбор 2','two']]:
            maps.insert(InlineKeyboardButton(i[0], callback_data=i[1]))
        return maps











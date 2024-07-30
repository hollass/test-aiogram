#! /usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import logging
from datetime import datetime

from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook

from database.db import users
from info.config import BOT_TOK, WEBHOOK_PORT, WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV, WEBHOOK_URL_BASE, \
    WEBHOOK_URL_PATH, WEBHOOK_HOST, NOTIFICATION_TIME

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO,
                    )
bot = Bot(BOT_TOK, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
mes = types.Message

us = users()

async def scheduler():
    while True:
        now = datetime.now()
        if now.hour == NOTIFICATION_TIME.hour and now.minute == NOTIFICATION_TIME.minute:
            for user_id in await us.get_users_id():
                await send_daily_reminder(user_id)
        await asyncio.sleep(60)

async def send_daily_reminder(chat_id: int):
    await bot.send_message(chat_id, "Не забудьте проверить уведомления!")
@dp.message_handler(commands='start')
async def startup(mes: mes):
    asyncio.create_task(scheduler())

    await mes.answer('Добро пожаловать в наш бот!')
    await us.add_table()

# Функция для начала работы вебхука
async def on_startup(dp):
    await bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))

# Функция для прекращения работы вебхука
async def on_shutdown(dp):
    await bot.delete_webhook()
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_URL_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBHOOK_HOST,
        port=WEBHOOK_PORT,
    )
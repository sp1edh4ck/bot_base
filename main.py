"""
The main file of the bot, it provides basic functions,
a database is connected, a base is made for creating
your own asynchronous functions, etc.

If you have any questions, you can send a telegram to @speedhack_support.
"""


import asyncio
import re
import time
from datetime import datetime, timedelta

import requests
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters.command import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message

import config
import markups as kb
from functions import base
from postgresql import Database
from translations import _


# A variable for calling functions, for example bot.send_message(...)
bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
# The variable is mainly for decorators or bot launch functions.
dp = Dispatcher()
# A variable for using the database
db = Database()


# Example of a class for FSMContext.
class Base(StatesGroup):
    base = State()


@dp.message(Command(commands=["s", "start"]))
async def command_start(message: Message, command: CommandObject):
    pass


@dp.message()
async def text_user(message: Message):
    """
    A function if the user has sent an unknown message/command.
    """
    lang = await db.get_lang(message.from_user.id)
    active = await db.get_active(message.from_user.id)
    if active:
        await message.reply(
            'Неизвестное сообщение. Попробуй написать /commands.'
        )
    else:
        await bot.send_message(
            message.from_user.id,
            '',
            reply_markup=kb.give_sub(lang).as_markup(),
            disable_web_page_preview=True
        )


async def main():
    """
    Launching the necessary functions in the bot,
    for example, creating tables in the database.
    """
    try:
        await db.connect()
        # A database method that cleans it up
        # every time the bot is launched
        # -------------------- #
        # await db.clear_all_tables()
        # -------------------- #
        await db.create_tables()
        await bot.delete_webhook(drop_pending_updates=True)
        await bot.send_message(
            config.ADMIN_IDS[0],
            '<b>The bot is running /start</b>'
        )
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    """
    The main function of launching the bot (asynchronously).
    """
    try:
        start_time = time.time()
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("\n\n" + "-" * 30)
        print("Бот остановлен")
        print(f"Время работы: {'%.2f' % (time.time() - start_time)}")
        print("-" * 30)

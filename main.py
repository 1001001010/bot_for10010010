from aiogram import executor
from handlers import dp
from other.bd_cfg import create_bdx
from maain import *
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import configparser
import datetime
import sqlite3
import re
from kb import *

# async def main():
# 	await dp.start_polling(bot)
# if __name__ == "__main__":
# 	asyncio.run(main())
# 	create_bdx()
if __name__ == "__main__":
    create_bdx()
    executor.start_polling(dp)

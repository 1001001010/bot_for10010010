from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
import configparser
import sqlite3


conn = sqlite3.connect('data.db')
cur = conn.cursor()

profile = types.InlineKeyboardMarkup(row_width=2)
profile.add(types.InlineKeyboardButton(text="Профиль", callback_data="profile"))
profile.add(types.InlineKeyboardButton(text="10010010", url='https://web.telegram.org/k/#@lll10010010'))

close = types.InlineKeyboardMarkup()
close.add(types.InlineKeyboardButton(text="закрыть", callback_data="close"))

start = types.InlineKeyboardMarkup()
start.add(types.InlineKeyboardButton(text="Начать", callback_data="start"))

work = types.InlineKeyboardMarkup(row_width=2)
work.add(types.InlineKeyboardButton(text="Тг-бот", callback_data="tg-bot"))
work.add(types.InlineKeyboardButton(text="Вк-бот", callback_data="vk-bot"))
work.add(types.InlineKeyboardButton(text="Discord-бот", callback_data="ds-bot"))
work.add(types.InlineKeyboardButton(text="Парсер", callback_data="parser"))
work.add(types.InlineKeyboardButton(text="Скрипт", callback_data="script"))
work.add(types.InlineKeyboardButton(text="WEB", callback_data="web"))

os = types.InlineKeyboardMarkup(row_width=3)
os.add(types.InlineKeyboardButton(text="Windows", callback_data="win"))
os.add(types.InlineKeyboardButton(text="macOS", callback_data="mac"))
os.add(types.InlineKeyboardButton(text="Linux", callback_data="lin"))

admin_panel = types.InlineKeyboardMarkup(row_width=2)
admin_panel.add(types.InlineKeyboardButton(text="WEB-админка", callback_data="web_admin"))
admin_panel.add(types.InlineKeyboardButton(text="Встроенная", callback_data="built_in"))
admin_panel.add(types.InlineKeyboardButton(text="Не нужна", callback_data="Need_not"))

admin_panel = types.InlineKeyboardMarkup(row_width=2)
admin_panel.add(types.InlineKeyboardButton(text="WEB-админка", callback_data="web_admin"))
admin_panel.add(types.InlineKeyboardButton(text="Встроенная", callback_data="built_in"))
admin_panel.add(types.InlineKeyboardButton(text="Не нужна", callback_data="Need_not"))

dostup = types.InlineKeyboardMarkup()
dostup.add(types.InlineKeyboardButton(text="🥷Доступ к тиме", callback_data="dostup_tim"))
# dostup.add(types.InlineKeyboardButton(text="❌✅Доступ к тиме", callback_data="dostup_tim"))
dostup.add(types.InlineKeyboardButton(text="📜Доступ к заказам", callback_data="dostup_zakaz"))

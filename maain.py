from aiogram import executor
from handlers import dp
from other.bd_cfg import create_bdx
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import configparser
import datetime
import sqlite3
import re
from kb import *
from loader import dp, bot
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from random import randint
from other.config import admin_channel_id
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from other.bd_cfg import *
import datetime
from handlers.user_main import *



config = configparser.ConfigParser()
config.read('config.ini')
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config['settings']['token'])
dp = Dispatcher(bot)
admin_id = int(config['settings']['admin_id'])

conn = sqlite3.connect('data.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users(
   tg_id INT,
   first_name TEXT,
   data TEXT,
   balance INT,
   UNIQUE ("tg_id") ON CONFLICT IGNORE
   );
""")
cur.execute("""CREATE TABLE IF NOT EXISTS application(
   tg_id INT,
   first_name TEXT,
   data TEXT,
   type TEXT,
   os TEXT, 
   admin TEXT,
   tz TEXT,
   dop TEXT,
   price INT,
   status TEXT,
   UNIQUE ("tg_id") ON CONFLICT IGNORE
   );
""")
cur.execute("""CREATE TABLE IF NOT EXISTS dostup(
   price INT,
   application INT,
   bot INT
   );
""")

# dostup = (1, 1, 1)
# cur.execute('INSERT INTO dostup VALUES(?, ?, ?)', dostup)
# conn.commit()


conn.commit()
@dp.message_handler(commands=("start"))
async def cmd_start(message: types.Message):
	if message.chat.id==admin_id:
		hello_keyboard_adm = types.ReplyKeyboardMarkup(resize_keyboard=True)
		button_1 = types.KeyboardButton(text="⛓️Доступ")
		button_2 = types.KeyboardButton(text="🥷Заявки")
		button_3 = types.KeyboardButton(text="📜Заказы")
		button_4 = types.KeyboardButton(text="➕Доп. меню")
		hello_keyboard_adm.add(button_1, button_2, button_3)
		hello_keyboard_adm.add(button_4)
		await bot.send_message(message.from_user.id, "текст для админа", reply_markup=hello_keyboard_adm)
	else:
		time = datetime.datetime.now()
		name = message.from_user.username
		user_list = (message.from_user.id, name, time, 0)
		cur.execute('INSERT INTO users VALUES(?, ?, ?, ?)', user_list)
		conn.commit()
		hello_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
		button_1 = types.KeyboardButton(text="📜Сделать заказ")
		button_2 = types.KeyboardButton(text="🥷Заявка в тиму")
		hello_keyboard.add(button_1, button_2)
		await bot.send_message(message.from_user.id, "こんにちは✋\nЯ помощник @lll10010010\nСначала выбери на клавиатуре, что тебе нужно↓", reply_markup=hello_keyboard)
		await bot.send_message(message.from_user.id, "Дополнительная инфа:", reply_markup=profile)

@dp.message_handler(lambda message: message.text == "📜Сделать заказ") 
async def without_puree(message: types.Message):
	dostup = """SELECT price from dostup"""
	cur.execute(dostup)
	records = str(cur.fetchall())
	dostup = records.replace('(', '').replace(')', '').replace(',', '').replace('[', '').replace(']', '')
	if dostup == "1":
		await bot.send_message(message.from_user.id, "💭Ответив на пару вопросов я помогу вам составить качественное тз\n❗Не забывай, что я могу отклонить ваше тз, НЕ ОБЪЯСНЯЯ ПРИЧИНЫ\n🕑Ответ приходит в бота в течении 24часов\n‍💼Если вы так и не получили ответ то пишите по контактам", reply_markup=start)
	if dostup == "0":
		await bot.send_message(message.from_user.id, "Сейчас эту функция закрыта администратором")

# @dp.message_handler(lambda message: message.text == "🥷Заявка в тиму")
# async def without_puree(message: types.Message):
# 	dostup = """SELECT application from dostup"""
# 	cur.execute(dostup)
# 	records = str(cur.fetchall())
# 	dostup = records.replace('(', '').replace(')', '').replace(',', '').replace('[', '').replace(']', '')
# 	if dostup == "1":
# 		await bot.send_message(message.from_user.id, "Сообщение для тимы")
# 	elif dostup == "0": 
# 		await bot.send_message(message.from_user.id, "Сейчас эту функция закрыта администратором")

@dp.message_handler(lambda message: message.text == "⛓️Доступ")
async def without_puree(message: types.Message):
	await bot.send_message(message.from_user.id, f"🚪Уровень доступа:", reply_markup=dostup)#Надо доделать


#коллбэк
@dp.callback_query_handler()
async def call_handler(call: types.CallbackQuery):
	if call.data == 'profile':
		data2 = str(cur.execute(f"SELECT data FROM users WHERE  tg_id ={call.from_user.id}").fetchone())
		data2 = data2.replace('(', '').replace(')', '').replace(',', '').replace("'", '').split('.')[0]
		user_profile = await bot.send_message(call.from_user.id, f"🥷 Ваш профиль, @{call.from_user.username}\n\nℹ️Telegram ID: {call.from_user.id}\n💁‍♂️Имя: @{call.from_user.username}\n⌚️Дата регистрации: {data2}\n", reply_markup=close)
	if call.data == 'close':
		await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
	if call.data == 'start':
		time = datetime.datetime.now()
		user_list = (call.from_user.id, call.from_user.username, time, 0, 0, 0, 0, 0, 0, 0)
		cur.execute('INSERT INTO application VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', user_list)
		conn.commit()
		await bot.send_message(call.from_user.id, "Сначала давайте определимся с типом работы", reply_markup=work)
#ТИП РАБОТЫ
	if call.data == 'tg-bot':
		await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
		type_tg_bot = f"""Update application set type = "tg-bot" where tg_id = {call.from_user.id}"""
		cur.execute(type_tg_bot)
		conn.commit()
		msg_types = await bot.send_message(call.from_user.id, "Вы выбрали telegram-бот\nДальше определимся c ОС\nВыберите вашу Операционную систему", reply_markup=os)
	if call.data == 'vk-bot':
		await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
		type_vk_bot = f"""Update application set type = "vk-bot" where tg_id = {call.from_user.id}"""
		cur.execute(type_vk_bot)
		conn.commit()
		msg_types = await bot.send_message(call.from_user.id, "Вы выбрали VK-бот\nДальше определимся c ОС\nВыберите вашу Операционную систему", reply_markup=os)
	if call.data == 'ds-bot':
		await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
		type_ds_bot = f"""Update application set type = "Discord-бот" where tg_id = {call.from_user.id}"""
		cur.execute(type_ds_bot)
		conn.commit()
		msg_types = await bot.send_message(call.from_user.id, "Вы выбрали Discord-бот\nДальше определимся c ОС\nВыберите вашу Операционную систему", reply_markup=os)
	if call.data == 'parser':
		await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
		type_parser = f"""Update application set type = "Парсер" where tg_id = {call.from_user.id}"""
		cur.execute(type_parser)
		conn.commit()
		msg_types = await bot.send_message(call.from_user.id, "Вы выбрали парсер\nДальше определимся c ОС\nВыберите вашу Операционную систему", reply_markup=os)
	if call.data == 'script':
		await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
		type_script = f"""Update application set type = "Скрипт" where tg_id = {call.from_user.id}"""
		cur.execute(type_script)
		conn.commit()
		msg_types = await bot.send_message(call.from_user.id, "Вы выбрали скрипт\nДальше определимся c ОС\nВыберите вашу Операционную систему", reply_markup=os)
	if call.data == 'web':
		await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
		type_web = f"""Update application set type = "WEB" where tg_id = {call.from_user.id}"""
		cur.execute(type_web)
		conn.commit()
		await bot.send_message(call.from_user.id, "Вы выбрали WEB\nДальше определимся c ОС\nВыберите вашу Операционную систему", reply_markup=os)
#Доступ
	if call.data == 'dostup_tim':
		dostup = """SELECT application from dostup"""
		cur.execute(dostup)
		records = str(cur.fetchall())
		dostup = records.replace('(', '').replace(')', '').replace(',', '').replace('[', '').replace(']', '')
		if dostup == "1":
			cur.execute("""Update dostup set application = "0" """)
			conn.commit()
			await bot.send_message(call.from_user.id, "❌Доступ к тиме закрыт", reply_markup=close)
		elif dostup == "0":
			cur.execute("""Update dostup set application = "1" """)
			await bot.send_message(call.from_user.id, "✅Доступ к тиме открыт", reply_markup=close)
	if call.data == 'dostup_zakaz':
		dostup = """SELECT price from dostup"""
		cur.execute(dostup)
		records = str(cur.fetchall())
		dostup = records.replace('(', '').replace(')', '').replace(',', '').replace('[', '').replace(']', '')
		if dostup == "1":
			cur.execute("""Update dostup set price = "0" """)
			await bot.send_message(call.from_user.id, "❌Доступ к заказам закрыт", reply_markup=close)
		elif dostup == "0":
			cur.execute("""Update dostup set price = "1" """)
			await bot.send_message(call.from_user.id, "✅Доступ к заказам открыт", reply_markup=close)
#OS
	if call.data == 'win':
		await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
		os_windows = f"""Update application set os = "windows" where tg_id = {call.from_user.id}"""
		cur.execute(os_windows)
		conn.commit()
		await bot.send_message(call.from_user.id, "Вы выбрали Windows\nДальше определимся с Админ-панелью\nВыберите подходящий вариант", reply_markup=admin_panel)
	if call.data == 'mac':
		await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
		os_macos = f"""Update application set os = "macOs" where tg_id = {call.from_user.id}"""
		cur.execute(os_macos)
		conn.commit()
		await bot.send_message(call.from_user.id, "Вы выбрали MacOs\nДальше определимся с Админ-панелью\nВыберите подходящий вариант", reply_markup=admin_panel)
	if call.data == 'lin':
		await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
		os_linux = f"""Update application set os = "Linux" where tg_id = {call.from_user.id}"""
		cur.execute(os_linux)
		conn.commit()
		await bot.send_message(call.from_user.id, "Вы выбрали Linux\nДальше определимся с Админ-панелью\nВыберите подходящий вариант", reply_markup=admin_panel)
#ТЗ
	if call.data == 'web_admin':
		await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
		web_admin = f"""Update application set admin = "WEB_admin" where tg_id = {call.from_user.id}"""
		cur.execute(web_admin)
		conn.commit()
		await bot.send_message(call.from_user.id, "Вы выбрали Web-Админку\nДальше мне нужно ваше тз(Техническое задание)\nНапишите в сообщении ваше тз")
		@dp.message_handler()
		async def echo_message(msg: types.Message):
			tz = str(msg.text)
			tz = f"""Update application set tz = {tz} where tg_id = {call.from_user.id}"""
			await bot.send_message(msg.from_user.id, "Хорошо, укажите желаемую цену:")
			@dp.message_handler()
			async def echo_message(msg: types.Message):
				price = f"""Update application set price = {msg.text} where tg_id = {call.from_user.id}"""


if __name__ == "__main__":
    create_bdx()
    executor.start_polling(dp)

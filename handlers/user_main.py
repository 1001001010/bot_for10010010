from loader import dp, bot
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from random import randint
from other.config import admin_channel_id
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from other.bd_cfg import *
import datetime


def get_dates():
    return datetime.datetime.today().replace(microsecond=0)


create_theme_kb = InlineKeyboardMarkup()
create_theme_kb.add(InlineKeyboardButton(text="Создать обращение", callback_data="create_theme"))


class UserMsg(StatesGroup):
    req_theme_name = State()
    req_text = State()
    req_id = State()


@dp.message_handler(commands="con", state="*")
async def cmd_start(message: types.Message, state: FSMContext):
    get_user_status = get_userx(user_id=message.from_user.id)
    try:
        if get_user_status[2] == "0" or get_user_status[2] is None:
            await message.answer(f"<b>Привет, <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>,"
                                 f" чтобы создать обращение к администратору, нажми на кноку \"Создать обращение\"</b>",
                                 reply_markup=create_theme_kb)
            get_user_id = get_userx(user_id=message.from_user.id)
            if get_user_id is None:
                add_userx(message.from_user.id, 0)
            else:
                await UserMsg.req_theme_name.set()
    except TypeError:
        await message.answer(
            f"<b>Привет, <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a>,"
            f" чтобы создать обращение к администратору, нажми на кноку \"Создать обращение\"</b>",
            reply_markup=create_theme_kb)
        get_user_id = get_userx(user_id=message.from_user.id)
        if get_user_id is None:
            add_userx(message.from_user.id, 0)
        else:
            await UserMsg.req_theme_name.set()


@dp.callback_query_handler(text="create_theme", state="*")
async def create_theme(call: types.CallbackQuery):
    get_user_status = get_userx(user_id=call.from_user.id)
    if get_user_status[2] == "0" or get_user_status[2] is None:
        await call.message.answer("<b>Введите тему вашего обращения:</b>")
        await UserMsg.req_theme_name.set()


@dp.message_handler(state=UserMsg.req_theme_name)
async def create_req_txt(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['req_theme_name'] = message.text
    await message.answer("<b>Введите текст обращения, чтобы прикрепить медиа файлы используйте ссылки с"
                         " <a href='anonfiles.com'>этого сайта (регистрация не нужна)</a> :</b>")
    await UserMsg.req_text.set()


confirm_theme_kb = InlineKeyboardMarkup()
confirm_theme_kb.add(InlineKeyboardButton(text="Подтвердить отправку", callback_data="send_theme"))
confirm_theme_kb.add(InlineKeyboardButton(text="Отменить отправку", callback_data="cancel_theme"))


@dp.message_handler(state=UserMsg.req_text)
async def confirm_req(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['req_text'] = message.text
    theme = data['req_theme_name']
    await message.answer(f"<b>Ваше обращение будет выглядеть так:\n\n"
                         f"Тема: <u>{theme}</u>\n"
                         f"Сообщение:\n<u>{message.text}</u></b>")
    await message.answer(f"<b>Подтвердить отправку данного обращения администратору?</b>",
                         reply_markup=confirm_theme_kb)

def send_theme_2_adm(req_id):
    send_answer_theme = InlineKeyboardMarkup()
    send_answer_theme.add(InlineKeyboardButton(text="Работать с обращением", callback_data=f"send_req:{req_id}"))
    print(req_id)
    return send_answer_theme


@dp.callback_query_handler(text="send_theme", state="*")
async def send_req(call: types.CallbackQuery, state: FSMContext):
    req_id = randint(100000, 999999)
    async with state.proxy() as data:
        data['req_id'] = req_id
    theme = data['req_theme_name']
    text = data['req_text']
    user_id = call.from_user.id
    user_first_name = call.from_user.first_name
    await call.message.edit_text(f"<b>Ваше обращение: <code>{theme}</code> // <code>id{req_id}</code> "
                                 f"было отправлено администратору, ожидайте ответа</b>")
    msg = f"<b>Новое обращение от: <a href='tg://user?id={user_id}'>{user_first_name}</a>\n\n" \
          f"Тема: <u>{theme}</u>\n\n" \
          f"Сообщение: {text}\n\n" \
          f"<code>id{req_id}</code> // <u>{get_dates()}</u></b>"
    await bot.send_message(chat_id=admin_channel_id, text=msg, reply_markup=send_theme_2_adm(req_id))
    add_requestx(user_id, user_first_name, theme, req_id, text, get_dates())
    await state.finish()

@dp.callback_query_handler(text="cancel_theme", state="*")
async def send_req(call: types.CallbackQuery):
    await call.message.edit_text("<b>Можете попробовать создать обращение ещё раз</b>", reply_markup=create_theme_kb)

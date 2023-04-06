from loader import dp, bot
from aiogram import types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from other.bd_cfg import *
from other.check_adm import IsAdmin


class SendUserMsg(StatesGroup):
    req_id = State()
    text_msg = State()
    yes_no = State()


def send_answer_2_user(req_id, user_id):
    req_menu_kb = InlineKeyboardMarkup()
    req_menu_kb.add(InlineKeyboardButton(text="Ответить на обращение", callback_data=f"answer_req:{req_id}"))
    req_menu_kb.add(InlineKeyboardButton(text="ban/unban", callback_data=f"user_menu:{user_id}"))
    return req_menu_kb


create_theme_kb = InlineKeyboardMarkup()
create_theme_kb.add(InlineKeyboardButton(text="Создать обращение", callback_data="create_theme"))


@dp.callback_query_handler(IsAdmin(), text_startswith="user_menu", state="*")
async def ban_user(call: types.CallbackQuery):
    user_id = call.data.split(":")[1]
    ban_user_kb = InlineKeyboardMarkup()
    ban_user_kb.add(InlineKeyboardButton(text="Забанить", callback_data=f"ban:{user_id}"))
    ban_user_kb.add(InlineKeyboardButton(text="Разбанить", callback_data=f"unban:{user_id}"))
    await call.message.answer(f"Подтвердите ban/unban пользователя <a href='tg://user?id={user_id}'>Username</a>",
                              reply_markup=ban_user_kb)


@dp.callback_query_handler(IsAdmin(), text_startswith="ban", state="*")
async def ban_user_sure(call: types.CallbackQuery):
    user_id = call.data.split(":")[1]
    update_userx(user_id, user_status=1)
    await call.message.edit_text(f"Пользователь забанен")
    await bot.send_message(chat_id=user_id, text=f"Вы были забанены")


@dp.callback_query_handler(IsAdmin(), text_startswith="unban", state="*")
async def ban_user_sure(call: types.CallbackQuery):
    user_id = call.data.split(":")[1]
    update_userx(user_id, user_status=0)
    await call.message.edit_text(f"Пользователь разбанен")
    await bot.send_message(chat_id=user_id, text=f"Вы были разбанены")


@dp.callback_query_handler(IsAdmin(), text_startswith="send_req", state="*")
async def req_menu(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    req_data = get_req(req_id=call.data.split(":")[1])
    user_id = req_data[1]
    user_fname = req_data[2]
    req_theme = req_data[3]
    req_id = req_data[4]
    req_txt = req_data[5]
    req_date = req_data[6]
    msg = f"<b>Вы выбрали обращение от пользователя: <a href='tg://user?id={user_id}'>{user_fname}</a>\n" \
          f"Текст обращения:\n\n{req_txt}\n\n" \
          f"<u>{req_date}</u> // <code>id{req_id}</code>\n" \
          f"Хотите ответить на данное обращение?</b>"
    await call.message.answer(f"<b>Перейдите в бота, для работы с обращением: <u>{req_theme}</u></b>")
    await bot.send_message(chat_id=call.from_user.id, text=msg,
                           reply_markup=send_answer_2_user(req_id=req_id, user_id=user_id))


@dp.callback_query_handler(IsAdmin(), text_startswith="answer_req")
async def send_answer_for_user(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['req_id'] = call.data.split(":")[1]
    req_data = get_req(req_id=call.data.split(":")[1])
    req_theme = req_data[3]
    req_id = req_data[4]
    await call.message.answer(f"<b>Введите ответ на обращение: {req_theme} // <code>id{req_id}</code></b>")
    await SendUserMsg.text_msg.set()


@dp.message_handler(state=SendUserMsg.text_msg)
async def confirm_send_answer(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text_msg'] = message.text
    req_id = data['req_id']
    req_data = get_req(req_id=req_id)
    user_id = req_data[1]
    user_fname = req_data[2]
    text = message.text
    confirm_send = InlineKeyboardMarkup()
    confirm_send.add(InlineKeyboardButton(text="Отправить ответ", callback_data="send_ans"))
    confirm_send.add(InlineKeyboardButton(text="Отменить отправку", callback_data=f"send_answer:{req_id}"))
    await message.answer(f"<b>Подтвердите отправку сообщения:\n\n"
                         f"{text}\n\n"
                         f"Пользователю:"
                         f"<a href='tg://user?id={user_id}'>{user_fname}</a></b>", reply_markup=confirm_send)


@dp.callback_query_handler(IsAdmin(), text="send_ans", state="*")
async def send_msg_2_user(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['yes_no'] = 1
    req_id = data['req_id']
    text = data['text_msg']
    req_data = get_req(req_id=req_id)
    user_id = req_data[1]
    req_theme = req_data[3]
    req_id = req_data[4]
    req_date = req_data[6]
    await call.message.answer(f"Сообщение было отправлено.")
    msg = f"Вам поступил ответ на обращение:\n" \
          f"<u>{req_theme}</u> // <code>id{req_id}</code> // <u>{req_date}</u>\n\n" \
          f"Сообщение от администратора:\n" \
          f"<b>{text}</b>"
    await bot.send_message(chat_id=user_id, text=msg, reply_markup=create_theme_kb)
    await state.finish()

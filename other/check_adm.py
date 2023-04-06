from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from other.config import admins


class IsAdmin(BoundFilter):
    async def check(self, message: types.Message):
        if str(message.from_user.id) in admins:
            return True
        else:
            return False
from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from utils.config import ADMIN_IDS


class IsAdmin(BoundFilter):

  async def check(self, message: types.Message):
    return message.from_user.id in 
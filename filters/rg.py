from aiogram.filters import Filter
from aiogram.types import Message

from services.api import api_manager


class GroupDirectorFilter(Filter):
    user_type = 'group_director'

    async def __call__(self, message: Message, *args, **kwargs):
        username = message.from_user.username
        user_type = api_manager.user_service.get_user_type(username)
        user_type = user_type.get('user_type', False)
        if not user_type:
            return False
        return user_type == self.user_type

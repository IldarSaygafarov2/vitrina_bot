from aiogram.filters import Filter
from aiogram.types import Message

from services.api import api_manager


class GroupDirectorFilter(Filter):
    user_type = 'group_director'

    async def __call__(self, message: Message, *args, **kwargs):
        username = message.from_user.username
        user_type = api_manager.user_service.get_user_type(username)
        if user_type == 'No User matches the given query.':
            return False
        return user_type['user_type'] == self.user_type

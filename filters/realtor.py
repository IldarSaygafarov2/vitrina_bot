from aiogram.filters import Filter
from aiogram.types import Message

from services.api import api_manager


class RealtorFilter(Filter):
    type = 'realtor'

    async def __call__(self, message: Message, *args, **kwargs):
        user_type = api_manager.user_service.get_user_type(message.from_user.username)
        if user_type == 'No User matches the given query.':
            return False
        return user_type['user_type'] == self.type

from .api import api_manager


class UserService:
    def is_user_realtor(self, tg_username: str) -> bool:
        """check is user realtor."""
        user_type = api_manager.user_service.get_user_type(tg_username)
        return user_type.get('user_type') == 'realtor'

    def is_user_rg(self, tg_username: str) -> bool:
        """check is user group director."""
        user_type = api_manager.user_service.get_user_type(tg_username)
        return user_type.get('user_type') == 'group_director'


user_manager = UserService()

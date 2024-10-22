# from aiogram import types, Router
# from aiogram.filters import Command
#
# from keyboards import reply, callback
# from services.api import api_manager
#
# router = Router(name='simple_user')
#
#
# @router.message(Command(commands=['start']))
# async def simple_user(message: types.Message):
#     current_user_username = message.from_user.username
#     realtors = api_manager.user_type.get_all_users_by_user_type(user_type='realtor')
#     if not realtors:
#         return await message.answer('Вас приветствует бот Vitrina')
#     realtors_usernames = list(map(lambda realtor: realtor['username'], realtors))
#     if current_user_username in realtors_usernames:
#         return await message.answer(f'Привет, риелтор: {current_user_username}',
#                                     reply_markup=reply.start_kb())
#
#     group_directors = api_manager.user_type.get_all_users_by_user_type(user_type='group_director')
#     if not group_directors:
#         return await message.answer('Вас приветствует бот Vitrina')
#     group_directors_usernames = list(map(lambda group_director: group_director['username'], group_directors))
#     if current_user_username in group_directors_usernames:
#         return await message.answer(f'Привет, руководитель группы: {current_user_username}',
#                                     reply_markup=callback.group_director_kb())
#
#     simple_admins = api_manager.user_type.get_all_users_by_user_type(user_type='simple_admin')
#     if not simple_admins:
#         return await message.answer('Вас приветствует бот Vitrina')
#     simple_admins_usernames = list(map(lambda simple_admin: simple_admin['username'], simple_admins))
#     if current_user_username in simple_admins_usernames:
#         return await message.answer(f'Привет, админ: {current_user_username}', )
#
#     await message.answer(f'Вас приветствует бот Vitrina')

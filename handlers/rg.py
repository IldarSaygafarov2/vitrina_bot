from aiogram import types, Router, F
from aiogram.filters import CommandStart

from keyboards import reply, callback

from services.api import api_manager
from services.user import user_manager


router = Router(name='rg_user')


@router.message(CommandStart(), F.func(lambda msg: user_manager.is_user_rg(msg.from_user.username)))
async def rg_start(message: types.Message):

    await message.answer(f'Привет, Руководитель группы', reply_markup=reply.rg_start_kb())


@router.message(F.text == 'Список риелторов')
async def rg_realtors(message: types.Message):
    res = api_manager.user_service.get_all_users(params={'user_type': 'group_director'})
    await message.answer('Список риелторов', reply_markup=callback.realtors_kb(res))


@router.callback_query(F.data.contains('realtor'))
async def rg_realtors_ads(callback_query: types.CallbackQuery):
    _, realtor_username, user_id = callback_query.data.split('_')


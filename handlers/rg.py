from aiogram import types, Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from keyboards import reply, callback
from services.api import api_manager
from services.user import user_manager
from services.utils import create_advertisement_message
from states.custom_states import RGProcessState

router = Router(name='rg_user')


@router.message(
    CommandStart(),
    F.func(lambda msg: user_manager.is_user_rg(msg.from_user.username))
)
async def rg_start(message: types.Message):
    await message.answer(f'Привет, Руководитель группы', reply_markup=reply.rg_start_kb())


@router.message(F.text == 'Список риелторов')
async def rg_realtors(message: types.Message):
    res = api_manager.user_service.get_all_users(params={'user_type': 'group_director'})
    await message.answer('Список риелторов', reply_markup=callback.realtors_kb(res))


@router.callback_query(F.data.contains('realtor'))
async def rg_realtors_ads(callback_query: types.CallbackQuery, state: FSMContext):
    _, realtor_username, user_id = callback_query.data.split('-')
    realtor_data = {
        'username': realtor_username,
        'realtor_id': user_id
    }
    await state.update_data(realtor_data=realtor_data)
    await state.set_state(RGProcessState.process_adverts)
    await callback_query.message.answer(f'Какие объявления показать', reply_markup=reply.ad_moderated_kb())


@router.message(
    RGProcessState.process_adverts,
    # F.text == 'Проверенные' | F.text == 'Нерповереные',
)
async def get_moderated_ads(message: types.Message, state: FSMContext):
    status = 'checked' if message.text == 'Проверенные' else 'unchecked'
    data = await state.get_data()
    user_id = int(data['realtor_data']['realtor_id'])
    username = data['realtor_data']['username']

    if status == 'checked':
        await state.set_state(RGProcessState.process_checked)
        await message.answer(f'Проверенные объявления риелтора: {username}')
        objects: list[dict] = api_manager.user_service.get_user_advertisements(user_id=user_id,
                                                                               params={'is_moderated': True})
        if not objects:
            await message.answer('Нет объявлений', )
            return
        for obj in objects:
            msg = create_advertisement_message(obj)
            await message.answer(msg)
    if status == 'unchecked':
        objects: list[dict] = api_manager.user_service.get_user_advertisements(user_id=user_id,
                                                                               params={'is_moderated': False})
        await message.answer(f'Непроверенные объявления риелтора: {username}')
        for obj in objects:
            msg = create_advertisement_message(obj)
            await message.answer(msg, reply_markup=callback.moderate_adv_kb(obj.get('id')))



@router.callback_query(F.data.contains('yes'))
async def moderate_ad_yes(callback_query: types.CallbackQuery, state: FSMContext):
    _, adv_id = callback_query.data.split('_')
    adv_id = int(adv_id)
    res = api_manager.advertiser_service.update_advertisement(adv_id, data={'is_moderated': True})
    await callback_query.message.answer('Объявление прошло проверку')


@router.callback_query(F.data.contains('no'))
async def moderate_ad_no(callback_query: types.CallbackQuery, state: FSMContext):
    _, adv_id = callback_query.data.split('_')
    print(adv_id)

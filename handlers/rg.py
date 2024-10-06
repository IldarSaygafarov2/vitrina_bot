from aiogram import types, Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from filters.rg import GroupDirectorFilter
from keyboards import callback
from keyboards.callback import ads_moderation_kb
from services.api import api_manager
from services.utils import create_advertisement_message
from states.custom_states import RGProcessState

router = Router(name='rg_user')


@router.message(
    CommandStart(),
    GroupDirectorFilter()
)
async def rg_start(message: types.Message):
    await message.answer(f'Привет, руководитель группы', reply_markup=callback.group_director_kb())


@router.callback_query(F.data == 'start_menu')
async def show_start_menu(
        call: types.CallbackQuery
):
    await call.answer()
    await call.message.edit_text(f'Привет, руководитель группы', reply_markup=callback.group_director_kb())


@router.callback_query(F.data == 'realtors_list')
async def show_realtors_menu(
        call: types.CallbackQuery
):
    await call.answer()
    realtors = api_manager.user_service.get_all_users(params={'user_type': 'realtor'})
    await call.message.edit_text(
        text='Список риелторов',
        reply_markup=callback.realtors_kb(realtors)
    )


@router.callback_query(F.data.startswith('realtor'))
async def rg_realtors_ads(
        call: types.CallbackQuery,
        state: FSMContext
):
    _, realtor_username, user_id = call.data.split(':')
    realtor_data = {
        'username': realtor_username,
        'realtor_id': user_id
    }
    await state.update_data(realtor_data=realtor_data)
    await state.set_state(RGProcessState.process_adverts)
    await call.message.edit_text(
        text='Какие объявления показать?',
        reply_markup=ads_moderation_kb()
    )


@router.callback_query(F.data == 'checked_ads')
async def show_checked_ads_menu(
        call: types.CallbackQuery,
        state: FSMContext
):
    # await call.answer()
    data = await state.get_data()
    data = data.get('realtor_data')

    params = {'is_moderated': True, 'user': data['realtor_id']}

    checked_ads = api_manager.advertiser_service.get_all(params=params).get('results')

    if not checked_ads:
        return await call.answer('Нет проверенных объявлений', show_alert=True)
    await call.message.edit_text(
        text='Проверенные объявления',
        reply_markup=callback.realtor_advertisements_kb(checked_ads, checked=True)
    )


@router.callback_query(F.data == 'unchecked_ads')
async def show_unchecked_ads_menu(
        call: types.CallbackQuery,
        state: FSMContext
):
    data = await state.get_data()
    realtor_data = data.get('realtor_data')
    params = {'is_moderated': False, 'user': realtor_data['realtor_id']}
    checked_ads = api_manager.advertiser_service.get_all(params=params).get('results')
    if not checked_ads:
        return await call.answer('Нет непроверенных объявлений', show_alert=True)
    await call.message.edit_text(
        text='Непроверенные объявления',
        reply_markup=callback.realtor_advertisements_kb(checked_ads, checked=False)
    )


@router.callback_query(F.data.startswith('unchecked_ad'))
async def show_unchecked_ads(
        call: types.CallbackQuery,
        state: FSMContext
):
    await call.answer()
    _, adv_id = call.data.split(':')

    advertisement = api_manager.advertiser_service.get_one(advertisement_id=int(adv_id))
    await state.update_data(advertisement=advertisement)
    await call.message.edit_text(
        text=create_advertisement_message(advertisement),
        reply_markup=callback.return_to_ads_kb(
            callback_data='unchecked_ads',
            adv_id=advertisement.get('id')
        )
    )


@router.callback_query(F.data.startswith('yes'))
async def confirm_advertisement_moderation(
        call: types.CallbackQuery,
        state: FSMContext
):
    # await call.answer()
    adv_id = int(call.data.split("_")[1])
    api_manager.advertiser_service.update_advertisement(adv_id, data={'is_moderated': True})
    await call.answer(f'Объявление успешно прошло модерацию', show_alert=True)
    await call.message.edit_text(
        text='Привет, руководитель группы',
        reply_markup=callback.group_director_kb()
    )


@router.callback_query(F.data.startswith('no'))
async def decline_advertisement_moderation(
        call: types.CallbackQuery,
        state: FSMContext
):
    adv_id = int(call.data.split("_")[1])

    await state.set_state(RGProcessState.process_unchecked)

    await call.message.edit_text(
        text='Напишите причину, почему данное объявление не прошло модерацию',
        reply_markup=callback.return_to_ads_kb('unchecked_ads', adv_id, show_checks=False)
    )


@router.message(RGProcessState.process_unchecked)
async def process_unchecked_ad(
        message: types.Message,
        state: FSMContext
):
    print(message.text)



#
# @router.message(
#     RGProcessState.process_adverts,
# )
# async def get_moderated_ads(message: types.Message, state: FSMContext):
#     status = 'checked' if message.text == 'Проверенные' else 'unchecked'
#     data = await state.get_data()
#     user_id = int(data['realtor_data']['realtor_id'])
#     username = data['realtor_data']['username']
#
#     if status == 'checked':
#         await state.set_state(RGProcessState.process_checked)
#         await message.answer(f'Проверенные объявления риелтора: {username}')
#         objects: list[dict] = api_manager.user_service.get_user_advertisements(user_id=user_id,
#                                                                                params={'is_moderated': True})
#         if not objects:
#             await message.answer('Нет объявлений')
#             return
#
#         for obj in objects:
#             msg = create_advertisement_message(obj)
#             await message.answer(msg)
#     if status == 'unchecked':
#         objects: list[dict] = api_manager.user_service.get_user_advertisements(user_id=user_id,
#                                                                                params={'is_moderated': False})
#         await message.answer(f'Непроверенные объявления риелтора: {username}')
#         for obj in objects:
#             msg = create_advertisement_message(obj)
#             await message.answer(msg, reply_markup=callback.moderate_adv_kb(obj.get('id')))
#
#
# @router.callback_query(F.data.contains('yes'))
# async def moderate_ad_yes(callback_query: types.CallbackQuery, state: FSMContext):
#     _, adv_id = callback_query.data.split('_')
#     adv_id = int(adv_id)
#     api_manager.advertiser_service.update_advertisement(adv_id, data={'is_moderated': True})
#     await callback_query.message.answer('Объявление прошло проверку')
#
#
# @router.callback_query(F.data.contains('no'))
# async def moderate_ad_no(callback_query: types.CallbackQuery, state: FSMContext):
#     _, adv_id = callback_query.data.split('_')
#     await state.set_state(RGProcessState.process_unchecked)
#     await state.update_data(adv_id=adv_id)
#     await callback_query.message.answer(f'Напишите причину, почему данное объвление не прошло модерацию')
#
#
# @router.message(
#     RGProcessState.process_unchecked
# )
# async def moderate_ad_unchecked(message: types.Message, state: FSMContext):
#     data = await state.get_data()
#     realtor_data = data['realtor_data']
#     text = message.text
#     await bot.send_message(chat_id=f'@{realtor_data["username"]}', text=text)
#
#
#

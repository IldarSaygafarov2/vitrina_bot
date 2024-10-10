from settings import BASE_DIR
from aiogram import types, Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from utils.advertisements import save_advertisements_photos
from filters.rg import GroupDirectorFilter
from keyboards import callback
from keyboards.callback import ads_moderation_kb
from services.api import api_manager
from services.utils import create_advertisement_message
from states.custom_states import RGProcessState
from templates.alert_texts import (
    no_unchecked_advertisements_alert, no_checked_advertisements_alert
)
from templates.rg_texts import (
    rg_welcome_text, rg_list_text, rg_advertisements_type_text, rg_checked_advertisements_text,
    rg_unchecked_advertisements_text, rg_advertisement_moderation_complete_text, rg_advertisement_decline_reason_text
)

router = Router(name='rg_user')


@router.message(
    GroupDirectorFilter(),
    CommandStart(),
)
async def rg_start(message: types.Message, state: FSMContext):
    await message.answer(rg_welcome_text(), reply_markup=callback.group_director_kb())


@router.callback_query(F.data == 'start_menu')
async def show_start_menu(
        call: types.CallbackQuery
):
    await call.answer()
    await call.message.edit_text(rg_welcome_text(), reply_markup=callback.group_director_kb())


@router.callback_query(F.data == 'realtors_list')
async def show_realtors_menu(
        call: types.CallbackQuery
):
    await call.answer()
    realtors = api_manager.user_service.get_all_users(params={'user_type': 'realtor'})
    await call.message.edit_text(
        text=rg_list_text(),
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
        text=rg_advertisements_type_text(),
        reply_markup=ads_moderation_kb()
    )


@router.callback_query(F.data == 'checked_ads')
async def show_checked_ads_menu(
        call: types.CallbackQuery,
        state: FSMContext
):
    data = await state.get_data()
    realtor_data = data.get('realtor_data')

    params = {'is_moderated': True, 'user': realtor_data['realtor_id']}

    checked_ads = api_manager.advertiser_service.get_all(params=params).get('results')

    if not checked_ads:
        return await call.answer(no_checked_advertisements_alert(), show_alert=True)
    await call.message.edit_text(
        text=rg_checked_advertisements_text(),
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
        return await call.answer(no_unchecked_advertisements_alert(), show_alert=True)
    await call.message.edit_text(
        text=rg_checked_advertisements_text(),
        reply_markup=callback.realtor_advertisements_kb(checked_ads, checked=False)
    )


@router.callback_query(F.data.startswith('unchecked_ad'))
async def show_unchecked_ads(
        call: types.CallbackQuery,
        state: FSMContext
):
    await call.answer()
    adv_id = int(call.data.split(':')[-1])

    advertisement = api_manager.advertiser_service.get_one(advertisement_id=adv_id)

    advertisement_photos = [obj.get('photo') for obj in advertisement.get('gallery')]

    save_advertisements_photos(
        photos=advertisement_photos,
        directory='photos'
    )

    await state.update_data(advertisement=advertisement)
    await call.message.edit_text(
        text=create_advertisement_message(advertisement),
        reply_markup=callback.return_to_ads_kb(
            callback_data='unchecked_ads',
            adv_id=advertisement.get('id')
        )
    )


@router.callback_query(F.data.startswith('checked_ad'))
async def show_checked_ads(
        call: types.CallbackQuery,
        state: FSMContext
):
    await call.answer()
    adv_id = int(call.data.split(':')[-1])

    advertisement = api_manager.advertiser_service.get_one(advertisement_id=adv_id)

    advertisement_photos = [obj.get('photo') for obj in advertisement.get('gallery')]

    await state.update_data(advertisement=advertisement)
    await call.message.edit_text(
        text=create_advertisement_message(advertisement),
        reply_markup=callback.return_to_ads_kb(
            callback_data='checked_ads',
            adv_id=advertisement.get('id'),
            show_checks=False
        )
    )


@router.callback_query(F.data.startswith('yes'))
async def confirm_advertisement_moderation(
        call: types.CallbackQuery,
        state: FSMContext
):
    adv_id = int(call.data.split("_")[1])
    api_manager.advertiser_service.update_advertisement(adv_id, data={'is_moderated': True})
    await call.answer(rg_advertisement_moderation_complete_text(), show_alert=True)
    await call.message.edit_text(
        text=rg_welcome_text(),
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
        text=rg_advertisement_decline_reason_text(),
        reply_markup=callback.return_to_ads_kb('unchecked_ads', adv_id, show_checks=False)
    )


@router.message(RGProcessState.process_unchecked)
async def process_unchecked_ad(
        message: types.Message,
        state: FSMContext
):
    state_data = await state.get_data()



    print(state_data)

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from keyboards import callback as callback_kb
from services.api import api_manager
from services.utils import create_advertisement_message
from settings import KB_FIELDS
from states.custom_states import AdvertisementEditingState
from templates.advertisements_texts import realtor_advertisement_editing_text

router = Router()


@router.callback_query(
    F.data.startswith('advertisement_update'),
    AdvertisementEditingState.start
)
async def update_advertisement(
        call: types.CallbackQuery,
        state: FSMContext
):
    await call.answer()
    state_data = await state.get_data()

    adv_id = int(call.data.split(':')[-1])
    advertisement = api_manager.advertiser_service.get_one(advertisement_id=adv_id)
    advertisement_message = create_advertisement_message(advertisement)

    await state.update_data(for_update=advertisement)
    await state.set_state(AdvertisementEditingState.process)
    await call.message.edit_text(
        text=advertisement_message,
        reply_markup=callback_kb.advertisement_fields_for_update_kb(adv_id)
    )


ADVERTISEMENT_RANGE_FIELDS = {
    'quadrature_from': 'Квадратура от',
    'quadrature_to': 'Квадратура до',
    'rooms_qty_from': 'Кол-во комнат от',
    'rooms_qty_to': 'Кол-во комнат до',
    'floor_from': 'Этаж от',
    'floor_to': 'Этаж до'
}

@router.callback_query(
    AdvertisementEditingState.process,
    F.data.startswith('field_update')
)
async def process_advertisement_fields_update(
        call: types.CallbackQuery,
        state: FSMContext
):
    await call.answer()

    state_data = await state.get_data()

    _, adv_id, callback  = call.data.split(':')
    field_call = callback.replace('update_', '')
    advertisement_for_update = state_data.get('for_update')
    current_value = {}
    for key, value in advertisement_for_update.items():
        if key == field_call:
            field_name = KB_FIELDS.get(callback)
            current_value[field_name] = value
        elif key.startswith(field_call):
            field_name = ADVERTISEMENT_RANGE_FIELDS.get(key)
            current_value[field_name] = value
    await call.message.edit_text(
        text=realtor_advertisement_editing_text(
            data=current_value,
        )
    )



@router.callback_query(
    AdvertisementEditingState.check,
    # F.data.startswith('update'),
)
async def process_advertisement_fields_check(
        call: types.CallbackQuery,
        state: FSMContext
):
    print(call.data)
    await call.answer()

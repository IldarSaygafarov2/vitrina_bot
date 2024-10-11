from pprint import pprint
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from keyboards import callback as callback_kb
from services.api import api_manager
from services.utils import create_advertisement_message
from states.custom_states import AdvertisementEditingState, AdvertisementUpdatingState
from templates.advertisement_editing_texts import update_advertisement_name_text, update_operation_type_text, \
    update_description_text, update_district_text, update_address_text, update_price_text, update_repair_type_text, \
    update_quadrature_text, update_rooms_text, update_floor_text, update_creation_date_text, \
    update_property_category_text, update_property_type_text
from settings import OPERATION_TYPES, ADVERTISEMENT_RANGE_FIELDS

router = Router()


@router.callback_query(F.data.startswith('advertisement_update'))
async def update_advertisement(
        call: types.CallbackQuery,
        state: FSMContext
):
    await call.answer()

    adv_id = int(call.data.split(':')[-1])
    advertisement = api_manager.advertiser_service.get_one(advertisement_id=adv_id)
    advertisement_message = create_advertisement_message(advertisement)

    await state.update_data(for_update=advertisement)
    await state.set_state(AdvertisementEditingState.process)
    await call.message.edit_text(
        text=advertisement_message,
        reply_markup=callback_kb.advertisement_fields_for_update_kb(adv_id)
    )


@router.callback_query(F.data.startswith('field_update'))
async def update_advertisement_editing(
        call: types.CallbackQuery,
        state: FSMContext
):
    await call.answer()

    state_data = await state.get_data()

    _, advertisement_id, field = call.data.split(':')
    advertisement = state_data.get('for_update')

    if field == 'update_name':
        msg = await call.message.edit_text(
            text=update_advertisement_name_text(
                advertisement_name=advertisement['name']
            ),
            reply_markup=callback_kb.return_back_kb(
                callback_data=f'advertisement_update:{advertisement_id}'
            )
        )
        await state.update_data(update_name=msg)
        await state.set_state(AdvertisementUpdatingState.update_name)

    elif field == 'update_operation_type':
        msg = await call.message.edit_text(
            text=update_operation_type_text(operation_type=advertisement['operation_type']),
            reply_markup=callback_kb.operation_type_kb(f'advertisement_update:{advertisement_id}')
        )
        await state.update_data(update_operation_type=msg)
        await state.set_state(AdvertisementUpdatingState.update_operation_type)
    elif field == 'update_gallery':
        pass
    elif field == 'update_description':
        msg = await call.message.edit_text(
            text=update_description_text(description=advertisement['description']),
            reply_markup=callback_kb.return_back_kb(
                callback_data=f'advertisement_update:{advertisement_id}'
            )
        )
        await state.update_data(update_description=msg)
        await state.set_state(AdvertisementUpdatingState.update_description)
    elif field == 'update_district':
        districts = api_manager.district_service.get_districts()
        msg = await call.message.edit_text(
            text=update_district_text(
                district_name=advertisement['district']['name']
            ),
            reply_markup=callback_kb.districts_kb(districts=districts,
                                                  callback_data=f'advertisement_update:{advertisement_id}')
        )
        await state.update_data(update_district=msg)
        await state.set_state(AdvertisementUpdatingState.update_district)
    elif field == 'update_address':
        msg = await call.message.edit_text(
            text=update_address_text(address=advertisement['address']),
            reply_markup=callback_kb.return_back_kb(
                callback_data=f'advertisement_update:{advertisement_id}'
            )
        )
        await state.update_data(update_address=msg)
        await state.set_state(AdvertisementUpdatingState.update_address)
    elif field == 'update_property_category':
        property_categories = api_manager.category_service.get_categories()
        msg = await call.message.edit_text(
            text=update_property_category_text(
                property_category=advertisement['category']['name'],
            ),
            reply_markup=callback_kb.property_categories_kb(
                categories=property_categories,
                callback_data=f'advertisement_update:{advertisement_id}',
                additional_callback='update'
            )
        )
        await state.update_data(update_property_category=msg)
        await state.set_state(AdvertisementUpdatingState.update_property_category)
    elif field == 'update_property_type':
        msg = await call.message.edit_text(
            text=update_property_type_text(
                property_type=advertisement['property_type'],
            ),
            reply_markup=callback_kb.property_type_kb(callback_data=f'advertisement_update:{advertisement_id}')
        )
        await state.update_data(update_property_type=msg)
        await state.set_state(AdvertisementUpdatingState.update_property_type)
    elif field == 'update_price':
        msg = await call.message.edit_text(
            text=update_price_text(current_price=advertisement['price']),
            reply_markup=callback_kb.return_back_kb(f'advertisement_update:{advertisement_id}')
        )
        await state.update_data(update_price=msg)
        await state.set_state(AdvertisementUpdatingState.update_price)
    elif field == 'update_quadrature':
        msg = await call.message.edit_text(
            text=update_quadrature_text(
                quadrature_from=advertisement['quadrature_from'],
                quadrature_to=advertisement['quadrature_to'],
            ),
            reply_markup=callback_kb.return_back_kb(f'advertisement_update:{advertisement_id}')
        )
        await state.update_data(update_quadrature=msg)
        await state.set_state(AdvertisementUpdatingState.update_quadrature)
    elif field == 'update_creation_date':
        msg = await call.message.edit_text(
            text=update_creation_date_text(
                current_creation_date=advertisement['creation_year']
            ),
            reply_markup=callback_kb.return_back_kb(f'advertisement_update:{advertisement_id}')
        )
        await state.update_data(update_creation_date=msg)
        await state.set_state(AdvertisementUpdatingState.update_creation_date)
    elif field == 'update_rooms':
        msg = await call.message.edit_text(
            text=update_rooms_text(
                rooms_from=advertisement['rooms_qty_from'],
                rooms_to=advertisement['rooms_qty_to'],
            ),
            reply_markup=callback_kb.return_back_kb(f'advertisement_update:{advertisement_id}')
        )
        await state.update_data(update_rooms=msg)
        await state.set_state(AdvertisementUpdatingState.update_rooms)
    elif field == 'update_floor':
        msg = await call.message.edit_text(
            text=update_floor_text(
                floor_from=advertisement['floor_from'],
                floor_to=advertisement['floor_to'],
            ),
            reply_markup=callback_kb.return_back_kb(f'advertisement_update:{advertisement_id}')
        )
        await state.update_data(update_floor=msg)
        await state.set_state(AdvertisementUpdatingState.update_floor)
    elif field == 'update_repair_type':
        msg = await call.message.edit_text(
            text=update_repair_type_text(repair_type=advertisement['repair_type']),
            reply_markup=callback_kb.advertisement_repair_type_kb(f'advertisement_update:{advertisement_id}')
        )
        await state.update_data(update_repair_type=msg)
        await state.set_state(AdvertisementUpdatingState.update_repair_type)
    elif field == 'update_house_quadrature':
        pass
    elif field == 'update_is_studio':
        pass


@router.message(AdvertisementUpdatingState.update_name)
async def process_update_name(
        message: types.Message,
        state: FSMContext
):
    print(message.text)


@router.callback_query(AdvertisementUpdatingState.update_operation_type)
async def process_update_operation_type(
        call: types.CallbackQuery,
        state: FSMContext
):
    await call.answer()

    print(call.data)


@router.message(AdvertisementUpdatingState.update_description)
async def process_update_description(
        message: types.Message,
        state: FSMContext
):
    print(message.text)


@router.callback_query(AdvertisementUpdatingState.update_district)
async def process_update_district(
        call: types.CallbackQuery,
        state: FSMContext
):
    await call.answer()
    print(call.data)


@router.message(AdvertisementUpdatingState.update_address)
async def process_update_address(
        message: types.Message,
        state: FSMContext
):
    print(message.text)


@router.message(AdvertisementUpdatingState.update_price)
async def process_update_price(
        message: types.Message,
        state: FSMContext
):
    print(message.text)


@router.callback_query(AdvertisementUpdatingState.update_repair_type)
async def process_update_repair_type(
        call: types.CallbackQuery,
        state: FSMContext
):
    await call.answer()
    print(call.data)


@router.message(AdvertisementUpdatingState.update_rooms)
async def process_update_rooms(
        message: types.Message,
        state: FSMContext
):
    print(message.text)


@router.message(AdvertisementUpdatingState.update_quadrature)
async def process_update_quadrature(
        message: types.Message,
        state: FSMContext
):
    print(message.text)


@router.message(AdvertisementUpdatingState.update_floor)
async def process_update_floor(
        message: types.Message,
        state: FSMContext
):
    print(message.text)


@router.message(AdvertisementUpdatingState.update_creation_date)
async def process_update_creation_date(
        message: types.Message,
        state: FSMContext
):
    print(message.text)


@router.callback_query(AdvertisementUpdatingState.update_property_category)
async def process_update_property_category(
        call: types.CallbackQuery,
        state: FSMContext
):
    await call.answer()
    print(call.data)


@router.callback_query(AdvertisementUpdatingState.update_property_type)
async def process_update_property_type(
        call: types.CallbackQuery,
        state: FSMContext
):
    await call.answer()
    print(call.data)

# @router.callback_query(
#     AdvertisementEditingState.process,
#     F.data.startswith('field_update')
# )
# async def process_advertisement_fields_update(
#         call: types.CallbackQuery,
#         state: FSMContext
# ):
#     await call.answer()
#
#     state_data = await state.get_data()
#     _, adv_id, callback = call.data.split(':')
#
#     print(callback)

# fields_for_update = state_data.get('fields_for_update')

# field_call = callback.replace('update_', '')
#
# advertisement_for_update = state_data.get('for_update')
#
# current_value = {}
#
# for key, value in advertisement_for_update.items():
#     if key == field_call:
#         field_name = KB_FIELDS.get(callback)
#         current_value[field_name] = value
#     elif key.startswith(field_call):
#         field_name = ADVERTISEMENT_RANGE_FIELDS.get(key)
#         current_value[field_name] = value
# msg = await call.message.edit_text(
#     text=realtor_advertisement_editing_text(
#         data=current_value if not fields_for_update else fields_for_update,
#     ),
#     reply_markup=callback_kb.return_back_kb(
#         callback_data=f'advertisement_update:{adv_id}'
#     )
# )
#
# await state.update_data(
#     field_name=field_call,
#     sent_message=msg,
#     fields_for_update=fields_for_update,
# )
#
# await state.set_state(AdvertisementEditingState.check)


# @router.message(
#     AdvertisementEditingState.check
# )
# async def process_advertisement_editing(
#         message: types.Message,
#         state: FSMContext
# ):
#     new_value = message.text
#
#     state_data = await state.get_data()
#     advertisement = state_data.get('for_update')
#     fields_for_update = state_data.get('fields_for_update')
#     field_name = state_data.get('field_name')
#
#     sent_message = state_data.get('sent_message')
#
#     if new_value == advertisement[field_name]:
#         msg = await sent_message.edit_text(
#             text=value_is_same_as_old_alert(),
#             reply_markup=callback_kb.return_back_kb(
#                 callback_data=f'field_update:{advertisement["id"]}:{field_name}'
#             )
#         )
#
#         await message.delete()
#         await state.set_state(AdvertisementEditingState.process)
#         await state.update_data(fields_for_update=fields_for_update, sent_message=msg)
#     else:
#         print(new_value)

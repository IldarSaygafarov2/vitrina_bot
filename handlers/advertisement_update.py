from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.utils.media_group import MediaGroupBuilder

from keyboards import callback as callback_kb
from keyboards import reply
from services.api import api_manager
from settings import OPERATION_TYPES, REPAIR_TYPES, PROPERTY_TYPES
from states.custom_states import AdvertisementEditingState, AdvertisementUpdatingState
from templates import advertisement_editing_texts as texts_of_update
from utils.advertisements import (
    save_advertisements_photos,
    create_advertisement_message,
    update_advertisement_text_field, save_photos_from_bot
)

router = Router()


@router.callback_query(F.data.startswith('advertisement_update'))
async def update_advertisement(
        call: types.CallbackQuery,
        state: FSMContext
):
    await call.answer()

    adv_id = int(call.data.split(':')[-1])
    advertisement = api_manager.advertiser_service.get_one(
        advertisement_id=adv_id
    )
    advertisement_message = create_advertisement_message(advertisement)

    await state.update_data(for_update=advertisement)
    await state.set_state(AdvertisementEditingState.process)
    msg = await call.message.edit_text(
        text=advertisement_message,
        reply_markup=callback_kb.advertisement_fields_for_update_kb(adv_id)
    )
    await state.update_data(starter_msg=msg)


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
            text=texts_of_update.update_advertisement_name_text(
                advertisement_name=advertisement['name']
            ),
            reply_markup=callback_kb.return_back_kb(
                callback_data=f'advertisement_update:{advertisement_id}'
            )
        )
        await state.update_data(update_name_msg=msg, advertisement_id=advertisement_id)
        await state.set_state(AdvertisementUpdatingState.update_name)

    elif field == 'update_operation_type':
        msg = await call.message.edit_text(
            text=texts_of_update.update_operation_type_text(
                operation_type=OPERATION_TYPES[advertisement['operation_type']]
            ),
            reply_markup=callback_kb.advertisement_choices_kb(
                choice_type='operation_type',
                callback_for_return=f'advertisement_update:{advertisement_id}',
                adv_id=advertisement_id
            )
        )
        await state.update_data(update_operation_type_msg=msg, advertisement_id=advertisement_id)
        await state.set_state(AdvertisementUpdatingState.update_operation_type)
    elif field == 'update_description':
        msg = await call.message.edit_text(
            text=texts_of_update.update_description_text(
                description=advertisement['description']),
            reply_markup=callback_kb.return_back_kb(
                callback_data=f'advertisement_update:{advertisement_id}'
            )
        )
        await state.update_data(update_description_msg=msg, advertisement_id=advertisement_id)
        await state.set_state(AdvertisementUpdatingState.update_description)
    elif field == 'update_district':
        districts = api_manager.district_service.get_districts()
        msg = await call.message.edit_text(
            text=texts_of_update.update_district_text(
                district_name=advertisement['district']['name']
            ),
            reply_markup=callback_kb.districts_kb(districts=districts,
                                                  callback_data=f'advertisement_update:{advertisement_id}')
        )
        await state.update_data(update_district_msg=msg, advertisement_id=advertisement_id)
        await state.set_state(AdvertisementUpdatingState.update_district)
    elif field == 'update_address':
        msg = await call.message.edit_text(
            text=texts_of_update.update_address_text(
                address=advertisement['address']),
            reply_markup=callback_kb.return_back_kb(
                callback_data=f'advertisement_update:{advertisement_id}'
            )
        )
        await state.update_data(update_address_msg=msg, advertisement_id=advertisement_id)
        await state.set_state(AdvertisementUpdatingState.update_address)
    elif field == 'update_property_category':
        property_categories = api_manager.category_service.get_categories()
        msg = await call.message.edit_text(
            text=texts_of_update.update_property_category_text(
                property_category=advertisement['category']['name'],
            ),
            reply_markup=callback_kb.property_categories_kb(
                categories=property_categories,
                callback_data=f'advertisement_update:{advertisement_id}',
                additional_callback='update'
            )
        )
        await state.update_data(update_property_category_msg=msg, advertisement_id=advertisement_id)
        await state.set_state(AdvertisementUpdatingState.update_property_category)
    elif field == 'update_property_type':
        msg = await call.message.edit_text(
            text=texts_of_update.update_property_type_text(
                property_type=advertisement['property_type'],
            ),
            reply_markup=callback_kb.advertisement_choices_kb(
                choice_type='property_type',
                callback_for_return=f'advertisement_update:{advertisement_id}',
                adv_id=advertisement_id
            )
        )
        await state.update_data(update_property_type_msg=msg, advertisement_id=advertisement_id)
        await state.set_state(AdvertisementUpdatingState.update_property_type)
    elif field == 'update_price':
        msg = await call.message.edit_text(
            text=texts_of_update.update_price_text(
                current_price=advertisement['price']),
            reply_markup=callback_kb.return_back_kb(
                f'advertisement_update:{advertisement_id}')
        )
        await state.update_data(update_price_msg=msg, advertisement_id=advertisement_id)
        await state.set_state(AdvertisementUpdatingState.update_price)
    elif field == 'update_quadrature':
        msg = await call.message.edit_text(
            text=texts_of_update.update_quadrature_text(
                quadrature_from=advertisement['quadrature_from'],
                quadrature_to=advertisement['quadrature_to'],
            ),
            reply_markup=callback_kb.return_back_kb(
                f'advertisement_update:{advertisement_id}')
        )
        await state.update_data(update_quadrature_msg=msg, advertisement_id=advertisement_id)
        await state.set_state(AdvertisementUpdatingState.update_quadrature)
    elif field == 'update_creation_date':
        msg = await call.message.edit_text(
            text=texts_of_update.update_creation_date_text(
                current_creation_date=advertisement['creation_year']
            ),
            reply_markup=callback_kb.return_back_kb(
                f'advertisement_update:{advertisement_id}')
        )
        await state.update_data(update_creation_date_msg=msg, advertisement_id=advertisement_id)
        await state.set_state(AdvertisementUpdatingState.update_creation_date)
    elif field == 'update_rooms':
        msg = await call.message.edit_text(
            text=texts_of_update.update_rooms_text(
                rooms_from=advertisement['rooms_qty_from'],
                rooms_to=advertisement['rooms_qty_to'],
            ),
            reply_markup=callback_kb.return_back_kb(
                f'advertisement_update:{advertisement_id}')
        )
        await state.update_data(update_rooms_msg=msg, advertisement_id=advertisement_id)
        await state.set_state(AdvertisementUpdatingState.update_rooms)
    elif field == 'update_floor':
        msg = await call.message.edit_text(
            text=texts_of_update.update_floor_text(
                floor_from=advertisement['floor_from'],
                floor_to=advertisement['floor_to'],
            ),
            reply_markup=callback_kb.return_back_kb(
                f'advertisement_update:{advertisement_id}')
        )
        await state.update_data(update_floor_msg=msg, advertisement_id=advertisement_id)
        await state.set_state(AdvertisementUpdatingState.update_floor)
    elif field == 'update_repair_type':
        msg = await call.message.edit_text(
            text=texts_of_update.update_repair_type_text(
                repair_type=advertisement['repair_type']),
            reply_markup=callback_kb.advertisement_choices_kb(
                choice_type='repair_type',
                callback_for_return=f'advertisement_update:{advertisement_id}',
                adv_id=advertisement_id
            )
        )
        await state.update_data(update_repair_type_msg=msg, advertisement_id=advertisement_id)
        await state.set_state(AdvertisementUpdatingState.update_repair_type)
    elif field == 'update_is_studio':
        msg = await call.message.edit_text(
            text=texts_of_update.update_is_studio_text(
                is_studio=advertisement['is_studio']),
            reply_markup=callback_kb.advertisement_is_studio_kb(
                callback_data_for_return=f'advertisement_update:{
                    advertisement_id}',
            )
        )
        await state.update_data(update_is_studio_msg=msg, advertisement_id=advertisement_id)
        await state.set_state(AdvertisementUpdatingState.update_is_studio)
    elif field == 'update_house_quadrature':
        msg = await call.message.edit_text(
            text=texts_of_update.update_house_quadrature_text(
                house_quadrature_from=advertisement['house_quadrature_from'],
                house_quadrature_to=advertisement['house_quadrature_to'],
            ),
            reply_markup=callback_kb.return_back_kb(
                f'advertisement_update:{advertisement_id}')
        )
        await state.update_data(update_house_quadrature_msg=msg, advertisement_id=advertisement_id)
        await state.set_state(AdvertisementUpdatingState.update_house_quadrature)
    elif field == 'update_gallery':
        starter_msg = state_data.get('starter_msg')

        gallery = api_manager.gallery.get_advertisement_gallery(
            advertisement_id=advertisement_id
        )

        if not gallery:
            return await call.answer('У данного объявления нет фотографий', show_alert=True)

        gallery_photos = [obj['photo'] for obj in gallery]
        saved_photos = save_advertisements_photos(gallery_photos, 'photos')

        media_group = MediaGroupBuilder(
            caption='Фотографии данного объявления')
        for saved_photo in saved_photos:
            media_group.add_photo(
                type='photo', media=types.FSInputFile(saved_photo))

        if starter_msg:
            await starter_msg.delete()

        msg = await call.message.answer_media_group(media=media_group.build())
        await call.message.answer(
            text='Выберите номер фотографии, которую хотите изменить',
            reply_markup=callback_kb.gallery_update_kb(
                gallery=gallery,
                callback_data_for_return=f'advertisement_update:{
                    advertisement_id}'
            )
        )

        await state.update_data(update_gallery_msg=msg,
                                advertisement_id=advertisement_id,
                                gallery=gallery,
                                saved_photos=saved_photos)
        await state.set_state(AdvertisementUpdatingState.update_gallery)


@router.message(AdvertisementUpdatingState.update_name)
async def process_update_name(
        message: types.Message,
        state: FSMContext
):
    """Update advertisement name."""
    await update_advertisement_text_field(
        message=message,
        state=state,
        state_field_name='update_name_msg',
        updating_field_name='name',
    )


@router.callback_query(AdvertisementUpdatingState.update_operation_type)
async def process_update_operation_type(
        call: types.CallbackQuery,
        state: FSMContext
):
    await call.answer()

    state_data = await state.get_data()
    msg = state_data.get('update_operation_type_msg')
    advertisement_id = state_data.get('advertisement_id')

    _, operation_type = call.data.split(':')
    api_manager.advertiser_service.update_advertisement(
        advertisement_id=advertisement_id,
        data={'operation_type': operation_type}
    )

    operation_type_text = OPERATION_TYPES[operation_type]

    await msg.edit_text(
        text=f'Тип операции успешно обовлен\n'
        f'Новое значение: <b>{operation_type_text}</b>',
        reply_markup=callback_kb.return_back_kb(
            f'advertisement_update:{advertisement_id}')
    )
    state_data.pop('update_operation_type_msg')


@router.message(AdvertisementUpdatingState.update_description)
async def process_update_description(
        message: types.Message,
        state: FSMContext
):
    await update_advertisement_text_field(
        message=message,
        state=state,
        state_field_name='update_description_msg',
        updating_field_name='description',
    )


@router.callback_query(AdvertisementUpdatingState.update_district)
async def process_update_district(
        call: types.CallbackQuery,
        state: FSMContext
):
    await call.answer()

    state_data = await state.get_data()
    advertisement_id = state_data.get('advertisement_id')
    msg = state_data.get('update_district_msg')

    _, district_slug = call.data.split('_')

    district_obj = api_manager.district_service.get_district(district_slug)
    api_manager.advertiser_service.update_advertisement(
        advertisement_id=advertisement_id,
        data={'district': district_obj['id']}
    )
    await msg.edit_text(
        text='Район успешно обновлен\n'
             f'Новое значение: <b><i>{district_obj["name"]}</i></b>',
        reply_markup=callback_kb.return_back_kb(
            f'advertisement_update:{advertisement_id}')
    )
    state_data.pop('update_district_msg')


@router.message(AdvertisementUpdatingState.update_address)
async def process_update_address(
        message: types.Message,
        state: FSMContext
):
    await update_advertisement_text_field(
        message=message,
        state=state,
        state_field_name='update_address_msg',
        updating_field_name='address',
    )


@router.message(AdvertisementUpdatingState.update_price)
async def process_update_price(
        message: types.Message,
        state: FSMContext
):
    await update_advertisement_text_field(
        message=message,
        state=state,
        state_field_name='update_price_msg',
        updating_field_name='price',
    )


@router.callback_query(AdvertisementUpdatingState.update_repair_type)
async def process_update_repair_type(
        call: types.CallbackQuery,
        state: FSMContext
):
    await call.answer()

    state_data = await state.get_data()
    advertisement_id = state_data.get('advertisement_id')
    msg = state_data.get('update_repair_type_msg')

    _, repair_type = call.data.split(':')

    api_manager.advertiser_service.update_advertisement(
        advertisement_id=advertisement_id,
        data={'repair_type': repair_type},
    )

    await msg.edit_text(
        text=f'''Данные успешно обновлены

Новое значение: <b><i>{REPAIR_TYPES[repair_type]}</i></b>
        ''',
        reply_markup=callback_kb.return_back_kb(
            f'advertisement_update:{advertisement_id}'
        )
    )
    state_data.pop('update_repair_type_msg')


@router.message(AdvertisementUpdatingState.update_rooms)
async def process_update_rooms(
        message: types.Message,
        state: FSMContext
):
    new_value = message.text.strip()
    rooms_qty_from, rooms_qty_to = new_value.split(',')

    await update_advertisement_text_field(
        message=message,
        state=state,
        state_field_name='update_rooms_msg',
        addon_fields={
            'rooms_qty_from': int(rooms_qty_from),
            'rooms_qty_to': int(rooms_qty_to)
        }
    )


@router.message(AdvertisementUpdatingState.update_quadrature)
async def process_update_quadrature(
        message: types.Message,
        state: FSMContext
):
    new_value = message.text.strip()
    quadrature_from, quadrature_to = new_value.split(',')

    await update_advertisement_text_field(
        message=message,
        state=state,
        state_field_name='update_quadrature_msg',
        addon_fields={
            'quadrature_from': int(quadrature_from),
            'quadrature_to': int(quadrature_to)
        }
    )


@router.message(AdvertisementUpdatingState.update_floor)
async def process_update_floor(
        message: types.Message,
        state: FSMContext
):
    new_value = message.text.strip()
    floor_from, floor_to = new_value.split(',')

    await update_advertisement_text_field(
        message=message,
        state=state,
        state_field_name='update_floor_msg',
        addon_fields={
            'floor_from': int(floor_from),
            'floor_to': int(floor_to)
        }
    )


@router.message(AdvertisementUpdatingState.update_creation_date)
async def process_update_creation_date(
        message: types.Message,
        state: FSMContext
):
    await update_advertisement_text_field(
        message=message,
        state=state,
        state_field_name='update_creation_date_msg',
        updating_field_name='creation_year',
    )


@router.callback_query(AdvertisementUpdatingState.update_property_category)
async def process_update_property_category(
        call: types.CallbackQuery,
        state: FSMContext
):
    await call.answer()

    state_data = await state.get_data()
    advertisement_id = state_data.get('advertisement_id')
    msg = state_data.get('update_property_category_msg')

    _, property_category_slug = call.data.split(':')
    property_category = api_manager.category_service.get_category(
        category_slug=property_category_slug
    )
    api_manager.advertiser_service.update_advertisement(
        advertisement_id=advertisement_id,
        data={'category': property_category['id']},
    )
    await msg.edit_text(
        text=f'''Данные успешно обновлены

Новое значение: <b><i>{property_category["name"]}</i></b>
        ''',
        reply_markup=callback_kb.return_back_kb(
            f'advertisement_update:{advertisement_id}'
        )
    )
    state_data.pop('update_property_category_msg')


@router.callback_query(AdvertisementUpdatingState.update_property_type)
async def process_update_property_type(
        call: types.CallbackQuery,
        state: FSMContext
):
    await call.answer()

    state_data = await state.get_data()
    advertisement_id = state_data.get('advertisement_id')
    msg = state_data.get('update_property_type_msg')

    _, property_type = call.data.split(':')

    api_manager.advertiser_service.update_advertisement(
        advertisement_id=advertisement_id,
        data={'property_type': property_type},
    )

    await msg.edit_text(
        text='Данные успешно обновлены!\n\n'
             f'Новое значение: <b><i>{PROPERTY_TYPES[property_type]}</i></b>',
        reply_markup=callback_kb.return_back_kb(
            f'advertisement_update:{advertisement_id}')
    )
    state_data.pop('update_property_type_msg')


@router.callback_query(AdvertisementUpdatingState.update_is_studio)
async def process_update_is_studio(
        call: types.CallbackQuery,
        state: FSMContext
):
    await call.answer()
    state_data = await state.get_data()
    advertisement_id = state_data.get('advertisement_id')
    msg = state_data.get('update_is_studio_msg')

    _, is_studio = call.data.split('_')

    is_studio = True if is_studio == 'yes' else False
    text = 'Да' if is_studio else 'Нет'
    api_manager.advertiser_service.update_advertisement(
        advertisement_id=advertisement_id,
        data={'is_studio': is_studio},
    )
    await msg.edit_text(
        text='Данные успешно изменены!!\n\n'
             f'Новое значение: <b><i>{text}</i></b>',
        reply_markup=callback_kb.return_back_kb(
            f'advertisement_update:{advertisement_id}')
    )
    state_data.pop('update_is_studio_msg')


@router.callback_query(AdvertisementUpdatingState.update_gallery)
async def process_update_gallery(
        call: types.CallbackQuery,
        state: FSMContext
):
    await call.answer()

    state_data = await state.get_data()
    advertisement_id = state_data.get('advertisement_id')
    gallery = state_data.get('gallery')

    _, gallery_photo_id = call.data.split(':')

    photo_for_update = [
        obj for obj in gallery if obj['id'] == int(gallery_photo_id)]
    msg_gallery = await call.message.edit_text(
        text='Отправьте новую фотографию',
        reply_markup=callback_kb.return_back_kb(
            f'advertisement_update:{advertisement_id}')
    )

    await state.update_data(msg_gallery=msg_gallery, photo_for_update=photo_for_update)
    await state.set_state(AdvertisementUpdatingState.update_gallery_photo)


@router.message(AdvertisementUpdatingState.update_gallery_photo)
async def process_update_gallery_photo(
        message: types.Message,
        state: FSMContext
):
    state_data = await state.get_data()
    advertisement_id = state_data.get('advertisement_id')
    new_photo = message.photo[-1].file_id
    photo_for_update = state_data.get('photo_for_update')
    file_names = await save_photos_from_bot(message, [new_photo])
    file = open(f'photos/{file_names[0]}', 'rb')
    res = api_manager.gallery.update_image_gallery(
        advertisement_id=advertisement_id,
        gallery_id=photo_for_update[0].get('id'),
        files={'photo': file},
        data={'advertisement': advertisement_id}
    )
    await message.answer(
        text='Фотография была успешно обновлена'
    )

    advertisement = api_manager.advertiser_service.get_one(advertisement_id)
    await message.answer(
        text=create_advertisement_message(advertisement),
        reply_markup=callback_kb.advertisement_fields_for_update_kb(
            advertisement_id)
    )


@router.message(AdvertisementUpdatingState.update_house_quadrature)
async def process_update_house_quadrature(
        message: types.Message,
        state: FSMContext
):
    new_value = message.text
    house_quadrature_from, house_quadrature_to = new_value.split(',')

    await update_advertisement_text_field(
        message=message,
        state=state,
        state_field_name='update_house_quadrature',
        addon_fields={
            'house_quadrature_from': house_quadrature_from,
            'house_quadrature_to': house_quadrature_to,
        }
    )


@router.callback_query(F.data == 'back_to_ads')
async def process_back_to_ads(
        call: types.CallbackQuery,
        state: FSMContext
):
    await call.answer()
    state_data = await state.get_data()
    realtor_id = state_data.get('realtor_id')

    user_advertisements = api_manager.user_service.get_user_advertisements(
        user_id=realtor_id)
    await call.message.edit_text(
        'Выберите объявление, которое хотите изменить',
        reply_markup=callback_kb.advertisements_for_update_kb(
            advertisements=user_advertisements)
    )


@router.callback_query(F.data == 'home_page_realtor')
async def home_page_realtor(
        call: types.CallbackQuery,
        state: FSMContext
):
    await call.answer()
    await call.message.delete()
    await call.message.answer(
        text='Выберите действие ниже',
        reply_markup=reply.start_kb()
    )

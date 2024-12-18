import os

from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto

from filters.realtor import RealtorFilter
from keyboards import callback as callback_kb
from keyboards import reply as kb
from services.api import api_manager
from settings import (
    REPAIR_TYPES_REVERSED,
    PROPERTY_TYPES_REVERSED,
    OPERATION_TYPES_REVERSED
)
from states.custom_states import AdvertisementState, AdvertisementEditingState
from templates import advertisements_texts as adv_texts
from utils.advertisements import save_photos_from_bot

router = Router(name='advertisement')


@router.message(CommandStart(), RealtorFilter())
async def cmd_start(message: types.Message):
    fullname = message.from_user.full_name
    user_id = api_manager.user_service.get_user_id(tg_username=message.from_user.username).get('id')
    res = api_manager.user_service.update_user_tg_user_id(
        user_id=user_id,
        data={'tg_user_id': message.from_user.id}
    )
    print(res)
    await message.answer(
        text=adv_texts.realtor_welcome_text(fullname),
        reply_markup=kb.start_kb()
    )


@router.message(F.text.lower() == 'создать объявление')
async def start_creating_ad(message: types.Message, state: FSMContext):
    await state.set_state(AdvertisementState.operation_type)
    await message.answer(
        text=adv_texts.realtor_operation_type_text(),
        reply_markup=kb.main_categories_kb()
    )


@router.message(AdvertisementState.operation_type)
async def process_main_categories(message: types.Message, state: FSMContext):
    categories = api_manager.category_service.get_categories()
    await state.update_data(operation_type=message.text)
    await state.set_state(AdvertisementState.property_category)
    await message.answer(
        text=adv_texts.realtor_property_category_text(),
        reply_markup=callback_kb.property_categories_kb(categories)
    )


@router.callback_query(AdvertisementState.property_category, F.data.startswith('property_category'))
async def process_photos_qty(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    _, category_slug = callback.data.split(':')
    category = api_manager.category_service.get_category(category_slug)
    category_uz = api_manager.category_service.get_category(category_slug, headers={'Accept-Language': 'uz'})

    await state.update_data(property_category=category, property_category_uz=category_uz)
    await state.set_state(AdvertisementState.photos_number)
    await callback.message.answer(
        text=adv_texts.realtor_selected_property_category_text(
            property_category=category.get('name')
        ))
    await callback.message.answer(
        text=adv_texts.realtor_photos_quantity_text(),
        reply_markup=types.ReplyKeyboardRemove()
    )


@router.message(AdvertisementState.photos_number)
async def process_photos_qty(message: types.Message, state: FSMContext):
    await state.update_data(photo_numbers=int(message.text), photos=[])
    await state.set_state(AdvertisementState.photos)
    await message.answer(
        text=adv_texts.realtor_photos_quantity_get_text()
    )


@router.message(AdvertisementState.photos)
async def process_photos(message: types.Message, state: FSMContext):
    current_state = await state.get_data()
    current_state['photos'].append(message.photo[-1].file_id)
    if current_state['photo_numbers'] == len(current_state['photos']):
        await state.update_data(photos=current_state['photos'])
        await state.set_state(AdvertisementState.title)
        await message.answer(
            text=adv_texts.realtor_title_text()
        )


@router.message(AdvertisementState.title)
async def process_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(AdvertisementState.title_uz)
    await message.answer(
        text='Напишите заголовок объявления на узбекском языке'
    )


@router.message(AdvertisementState.title_uz)
async def process_title_uz(message: types.Message, state: FSMContext):
    await state.update_data(title_uz=message.text)
    await state.set_state(AdvertisementState.full_description)
    await message.answer(
        text=adv_texts.realtor_description_text()
    )


@router.message(AdvertisementState.full_description)
async def process_description(message: types.Message, state: FSMContext):
    await state.update_data(full_description=message.text)
    await state.set_state(AdvertisementState.full_description_uz)
    await message.answer(
        text='Напишите описание для объявления на узбекском языке',
    )


@router.message(AdvertisementState.full_description_uz)
async def process_description_uz(message: types.Message, state: FSMContext):
    districts = api_manager.district_service.get_districts()
    await state.update_data(full_description_uz=message.text)
    await state.set_state(AdvertisementState.district)
    await message.answer(
        text=adv_texts.realtor_choose_district_text(),
        reply_markup=callback_kb.districts_kb(districts)
    )


@router.callback_query(AdvertisementState.district, F.data.startswith('district'))
async def process_district(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    data = await state.get_data()

    _, district_slug = callback.data.split('_')
    district = api_manager.district_service.get_district(district_slug)
    district_uz = api_manager.district_service.get_district(district_slug, headers={'Accept-Language': 'uz'})

    await state.update_data(district=district, district_uz=district_uz)
    await callback.message.answer(
        text=adv_texts.realtor_chosen_district_text(
            district=district.get('name')
        )
    )

    property_category = data['property_category']['slug']
    if property_category == 'doma':
        await state.set_state(AdvertisementState.house_quadrature_from)
        await callback.message.answer(
            text=adv_texts.realtor_quadrature_of_house_from()
        )
    else:
        await state.set_state(AdvertisementState.address)
        await callback.message.answer(
            text=adv_texts.realtor_correct_address_text()
        )


@router.message(AdvertisementState.house_quadrature_from)
async def process_house_quadrature_from(message: types.Message, state: FSMContext):
    await state.update_data(house_quadrature_from=int(message.text))
    await state.set_state(AdvertisementState.house_quadrature_to)
    await message.answer(
        text=adv_texts.realtor_quadrature_of_house_to()
    )


@router.message(AdvertisementState.house_quadrature_to)
async def process_house_quadrature_to(message: types.Message, state: FSMContext):
    await state.update_data(house_quadrature_to=int(message.text))
    await state.set_state(AdvertisementState.address)
    await message.answer(
        text=adv_texts.realtor_correct_address_text()
    )


@router.message(AdvertisementState.address)
async def process_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    await state.set_state(AdvertisementState.address_uz)
    await message.answer(
        text='Напишите адрес объявления на узбекском языке',
    )


@router.message(AdvertisementState.address_uz)
async def process_address_uz(message: types.Message, state: FSMContext):
    await state.update_data(address_uz=message.text)
    await state.set_state(AdvertisementState.property_type)
    await message.answer(
        text=adv_texts.realtor_property_type_text(),
        reply_markup=kb.property_type_kb()
    )


@router.message(AdvertisementState.property_type)
async def process_property(message: types.Message, state: FSMContext):
    await state.update_data(property_type=message.text)
    if message.text == 'Новостройка':
        await state.set_state(AdvertisementState.creation_date)
        await message.answer(
            text=adv_texts.realtor_property_creation_year_text()
        )
    elif message.text == 'Вторичный фонд':
        await state.set_state(AdvertisementState.price)
        await state.update_data(creation_date=0)
        await message.answer(
            text=adv_texts.realtor_price_text(),
            reply_markup=types.ReplyKeyboardRemove()
        )


@router.message(AdvertisementState.creation_date)
async def process_creation_date(message: types.Message, state: FSMContext):
    await state.update_data(creation_date=message.text)
    await state.set_state(AdvertisementState.price)
    await message.answer(
        text=adv_texts.realtor_price_text(),
        reply_markup=types.ReplyKeyboardRemove()
    )


@router.message(AdvertisementState.price)
async def process_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    await state.set_state(AdvertisementState.auction_allowed)
    await message.answer(
        text=adv_texts.realtor_is_auction_allowed_text(),
        reply_markup=kb.is_auction_allowed_kb()
    )


@router.message(AdvertisementState.auction_allowed)
async def process_auction_allowed(message: types.Message, state: FSMContext):
    data = await state.get_data()
    property_category = data['property_category']['slug']

    is_allowed = True if message.text == 'Да' else False
    await state.update_data(auction_allowed=is_allowed)

    if property_category == 'doma':
        await state.set_state(AdvertisementState.rooms_from)
        return await message.answer(
            text=adv_texts.realtor_rooms_from_to_text(
                is_from=True
            )
        )

    await state.set_state(AdvertisementState.is_studio)
    await message.answer(
        text=adv_texts.realtor_is_property_studio_text(),
        reply_markup=kb.is_studio_kb()
    )


@router.message(AdvertisementState.is_studio)
async def process_is_studio(message: types.Message, state: FSMContext):
    if message.text == 'Да':
        await state.update_data(is_studio=True)
        await state.set_state(AdvertisementState.quadrature_from)
        await message.answer(
            text=adv_texts.realtor_quadrature_from_to_text(is_from=True)
        )
    else:
        await state.update_data(is_studio=False)
        await state.set_state(AdvertisementState.rooms_from)
        await message.answer(
            text=adv_texts.realtor_rooms_from_to_text(
                is_from=True
            )
        )


@router.message(AdvertisementState.rooms_from)
async def process_rooms(message: types.Message, state: FSMContext):
    await state.update_data(rooms_from=message.text)
    await state.set_state(AdvertisementState.rooms_to)
    await message.answer(
        text=adv_texts.realtor_rooms_from_to_text(
            is_from=False
        )
    )


@router.message(AdvertisementState.rooms_to)
async def process_rooms(message: types.Message, state: FSMContext):
    await state.update_data(rooms_to=message.text)
    await state.set_state(AdvertisementState.quadrature_from)
    await message.answer(
        text=adv_texts.realtor_quadrature_from_to_text(is_from=True)
    )


@router.message(AdvertisementState.quadrature_from)
async def process_quadrature(message: types.Message, state: FSMContext):
    await state.update_data(quadrature_from=message.text)
    await state.set_state(AdvertisementState.quadrature_to)
    await message.answer(
        text=adv_texts.realtor_quadrature_from_to_text(is_from=False)
    )


@router.message(AdvertisementState.quadrature_to)
async def process_quadrature(message: types.Message, state: FSMContext):
    await state.update_data(quadrature_to=message.text)
    await state.set_state(AdvertisementState.floor_from)
    await message.answer(
        text=adv_texts.realtor_floor_from_to_text(is_from=True)
    )


@router.message(AdvertisementState.floor_from)
async def process_floor(message: types.Message, state: FSMContext):
    await state.update_data(floor_from=message.text)
    await state.set_state(AdvertisementState.floor_to)
    await message.answer(
        text=adv_texts.realtor_floor_from_to_text(is_from=False)
    )


@router.message(AdvertisementState.floor_to)
async def process_floor(message: types.Message, state: FSMContext):
    await state.update_data(floor_to=message.text)
    await state.set_state(AdvertisementState.repair_type)
    await message.answer(
        text=adv_texts.realtor_advertisement_repair_type_text(),
        reply_markup=kb.repair_type_kb()
    )


@router.message(AdvertisementState.repair_type)
async def process_repair(message: types.Message, state: FSMContext):
    data = await state.get_data()

    title = data.get('title')
    description = data.get('full_description')
    address = data.get('address')

    address_uz = data.get('address_uz')
    title_uz = data.get('title_uz')
    description_uz = data.get('full_description_uz')

    is_allowed = data.get('auction_allowed')
    property_category = data.get('property_category')
    property_category_uz = data.get('property_category_uz')
    operation_type = data.get('operation_type')

    district = data.get('district')
    district_uz = data.get('district_uz')

    property_type = data.get('property_type')

    repair_type = message.text

    price = data.get('price')
    rooms_from = data.get('rooms_from', 0)
    rooms_to = data.get('rooms_to', 0)
    quadrature_from = data.get('quadrature_from')
    quadrature_to = data.get('quadrature_to')
    floor_from = data.get('floor_from')
    floor_to = data.get('floor_to')

    is_studio = data.get('is_studio')
    creation_date = data.get('creation_date')

    house_quadrature_from = data.get('house_quadrature_from')
    house_quadrature_to = data.get('house_quadrature_to')



    username = message.from_user.username
    user_id = api_manager.user_service.get_user_id(username)

    file_names = await save_photos_from_bot(message, data['photos'])

    operation_type_key = OPERATION_TYPES_REVERSED[operation_type]
    property_type_key = PROPERTY_TYPES_REVERSED[property_type]
    repair_type_key = REPAIR_TYPES_REVERSED[repair_type]

    msg = adv_texts.realtor_advertisement_completed_text(
        title=title,
        operation_type=operation_type,
        description=description,
        district=district['name'],
        address=address,
        property_category=property_category['name'],
        property_type=property_type,
        price=price,
        quadrature_from=quadrature_from,
        quadrature_to=quadrature_to,
        creation_date=creation_date,
        rooms_from=rooms_from,
        rooms_to=rooms_to,
        floor_from=floor_from,
        floor_to=floor_to,
        repair_type=repair_type,
        house_quadrature_from=house_quadrature_from,
        house_quadrature_to=house_quadrature_to,
        is_studio=is_studio,
    )

    media: list[InputMediaPhoto] = [
        InputMediaPhoto(media=img, caption=msg) if i == 0 else InputMediaPhoto(media=img)
        for i, img in enumerate(data['photos'])
    ]

    new = api_manager.advertiser_service.create_advertisement(
        data={
            "name": title,
            "description": description,
            "district": district['id'],
            'operation_type': operation_type_key,
            'operation_type_uz': operation_type_key,
            "address": address,
            "property_type": property_type_key,
            "property_type_uz": property_type_key,
            "price": price,
            "rooms_qty_from": rooms_from,
            "rooms_qty_to": rooms_to,
            "quadrature_from": quadrature_from,
            "quadrature_to": quadrature_to,
            "floor_from": floor_from,
            "floor_to": floor_to,
            "auction_allowed": is_allowed,
            "category": property_category['id'],
            'repair_type': repair_type_key,
            'repair_type_uz': repair_type_key,
            'house_quadrature_from': house_quadrature_from,
            'house_quadrature_to': house_quadrature_to,
            'is_studio': is_studio,
            'user': user_id['id'],
        },
    )
    print(new)

    try:
        api_manager.advertiser_service.update_advertisement(
            advertisement_id=new['id'],
            data={
                'name': title_uz,
                'description': description_uz,
                'address': address_uz,
                'district': district_uz['id'],
                'category': property_category_uz['id'],
            },
            headers={
                'Accept-Language': 'uz',
            }
        )
    except Exception as e:
        print(e, e.__class__)


    media_files = os.listdir('photos')
    for media_file in media_files:
        if media_file not in file_names:
            continue

        file = open(f'photos/{media_file}', 'rb')
        media_data = {'photo': file}
        data = {'advertisement': new['id']}
        res = api_manager.gallery.upload_image_to_gallery(
            advertisement_id=new['id'],
            files=media_data,
            data=data
        )

    await message.answer_media_group(media=media)
    await state.clear()
    await message.answer(
        text=adv_texts.realtor_choose_action_below_text(),
        reply_markup=kb.start_kb()
    )


@router.message(
    F.text.lower() == 'мои объявления',
    RealtorFilter()
)
async def process_realtor_advertisements(
        message: types.Message,
        state: FSMContext
):
    username = message.from_user.username
    user_id = api_manager.user_service.get_user_id(
        tg_username=username
    ).get('id')

    user_advertisements = api_manager.user_service.get_user_advertisements(user_id=user_id)

    await state.set_state(AdvertisementEditingState.start)

    await message.answer(
        'Выберите действие ниже',
        reply_markup=callback_kb.advertisements_of_realtor_kb(user_id)
    )
    await state.update_data(realtor_id=user_id, user_advertisements=user_advertisements)


@router.callback_query(F.data.startswith('moderation_completed_advertisements'))
async def show_moderation_completed_advertisements(
        call: types.CallbackQuery,
        state: FSMContext
):
    state_data = await state.get_data()
    realtor_id = state_data.get('realtor_id')
    realtor_all_advertisements = api_manager.user_service.get_user_advertisements(user_id=realtor_id,
                                                                                  params={'is_moderated': True})
    if not realtor_all_advertisements:
        return await call.answer('Нет проверенных объявлений', show_alert=True)

    moderation_completed_advertisements = list(filter(lambda adv: adv['is_moderated'], realtor_all_advertisements))
    if not moderation_completed_advertisements:
        return await call.answer('Нет проверенных объявлений', show_alert=True)

    await call.message.edit_text(
        text='Выберите объявление',
        reply_markup=callback_kb.advertisements_for_update_kb(advertisements=moderation_completed_advertisements)
    )


@router.callback_query(F.data.startswith('moderation_failed_advertisements'))
async def show_moderation_failed_advertisements(
        call: types.CallbackQuery,
        state: FSMContext
):
    state_data = await state.get_data()
    realtor_id = state_data.get('realtor_id')
    realtor_moderation_failed_advertisements = api_manager.user_service.get_user_advertisements(
        user_id=realtor_id,
        params={'is_moderated': False}
    )
    if not realtor_moderation_failed_advertisements:
        return await call.answer('Все объявления прошли проверку', show_alert=True)

    await call.message.edit_text(
        text='Выберите объявление, непрошедшее модерацию, чтобы узнать причину',
        reply_markup=callback_kb.advertisements_rejection_reasons_kb(realtor_moderation_failed_advertisements)
    )


@router.callback_query(F.data.startswith('rejection_reason'))
async def show_rejection_reason(
        call: types.CallbackQuery,
        state: FSMContext
):
    _, realtor_id, advertisement_id = call.data.split(':')
    realtor_id, advertisement_id = int(realtor_id), int(advertisement_id)

    moderation_objects = api_manager.moderation.get_realtor_advertisements_for_moderation(realtor_id)
    moderation_objects_for_advertisements = list(filter(lambda obj: obj['advertisement'] == advertisement_id
                                                                    and obj['rejection_reason'] is not None,
                                                        moderation_objects))
    if not moderation_objects_for_advertisements:
        return await call.message.edit_text(
            text='Причины отказа еще не добавлены для этого объявления\n\nВыберите действие ниже',
            reply_markup=callback_kb.advertisements_of_realtor_kb(realtor_id)
        )

    advertisement_rejections = "Причины отказа:\n\n"
    for idx, obj in enumerate(moderation_objects_for_advertisements, start=1):
        advertisement_rejections += f"{idx}. {obj['rejection_reason']}\n"

    await call.message.edit_text(
        text=advertisement_rejections,
    )
    await call.message.answer(
        text='Выберите действие ниже',
        reply_markup=callback_kb.advertisements_of_realtor_kb(realtor_id)

    )


@router.callback_query(F.data.startswith('all_advertisements'))
async def show_realtor_all_advertisements(
        call: types.CallbackQuery,
        state: FSMContext
):
    _, realtor_id = call.data.split(':')
    realtor_all_advertisements = api_manager.user_service.get_user_advertisements(
        user_id=realtor_id,
    )
    if not realtor_all_advertisements:
        return await call.answer('Вы еще не добавили объявления', show_alert=True)

    await call.message.edit_text(
        text='Выберите объявление',
        reply_markup=callback_kb.advertisements_for_update_kb(advertisements=realtor_all_advertisements)
    )

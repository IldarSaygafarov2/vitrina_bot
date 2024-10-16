import os

from aiogram import Router, types, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import InputMediaPhoto

from filters.realtor import RealtorFilter
from keyboards import callback as callback_kb
from keyboards import reply as kb
from services.api import api_manager
from services.utils import get_repair_type_by_name, get_property_type
from states.custom_states import AdvertisementState, AdvertisementEditingState
from templates import advertisements_texts as adv_texts

router = Router(name='advertisement')


@router.message(CommandStart(), RealtorFilter())
async def cmd_start(message: types.Message):
    fullname = message.from_user.full_name
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


@router.callback_query(F.data.startswith('property_category'))
@router.message(AdvertisementState.property_category)
async def process_photos_qty(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    _, category_slug = callback.data.split(':')
    category = api_manager.category_service.get_category(category_slug)

    await state.update_data(property_category=category)
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
    await state.set_state(AdvertisementState.full_description)
    await message.answer(
        text=adv_texts.realtor_description_text()
    )


@router.message(AdvertisementState.full_description)
async def process_description(message: types.Message, state: FSMContext):
    districts = api_manager.district_service.get_districts()
    await state.update_data(full_description=message.text)
    await state.set_state(AdvertisementState.district)
    await message.answer(
        text=adv_texts.realtor_choose_district_text(),
        reply_markup=callback_kb.districts_kb(districts)
    )


# @router.message(AdvertisementState.district)
@router.callback_query(AdvertisementState.district, F.data.startswith('district'))
async def process_district(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()

    data = await state.get_data()

    _, district_slug = callback.data.split('_')
    district = api_manager.district_service.get_district(district_slug)

    await state.update_data(district=district)
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
    is_allowed = data.get('auction_allowed')
    property_category = data.get('property_category')
    operation_type = data.get('operation_type')
    description = data.get('full_description')
    district = data.get('district')
    property_type = data.get('property_type')
    price = data.get('price')
    rooms_from = data.get('rooms_from', 0)
    rooms_to = data.get('rooms_to', 0)
    quadrature_from = data.get('quadrature_from')
    quadrature_to = data.get('quadrature_to')
    floor_from = data.get('floor_from')
    floor_to = data.get('floor_to')
    repair_type = message.text
    is_studio = data.get('is_studio')
    creation_date = data.get('creation_date')
    address = data.get('address')
    house_quadrature_from = data.get('house_quadrature_from')
    house_quadrature_to = data.get('house_quadrature_to')
    file_names = []

    for photo in data['photos']:
        file = await message.bot.get_file(photo)
        file_path = file.file_path
        file_names.append(file_path.split('/')[-1])
        await message.bot.download_file(file_path, f'photos/{file_path.split("/")[-1]}')

    repair_type_choice = get_repair_type_by_name(repair_type)
    property_type_choice = get_property_type(property_type)

    username = message.from_user.username
    user_id = api_manager.user_service.get_user_id(username)

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
            "address": address,
            "property_type": property_type_choice,
            "price": price,
            "rooms_qty_from": rooms_from,
            "rooms_qty_to": rooms_to,
            "quadrature_from": quadrature_from,
            "quadrature_to": quadrature_to,
            "floor_from": floor_from,
            "floor_to": floor_to,
            "auction_allowed": is_allowed,
            "category": property_category['id'],
            'repair_type': repair_type_choice,
            'house_quadrature_from': house_quadrature_from,
            'house_quadrature_to': house_quadrature_to,
            'is_studio': is_studio,
            'user': user_id['id'],
        },
    )
    print(new)
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
    user_id = api_manager.user_service.get_user_id(
        tg_username=message.from_user.username
    ).get('id')

    user_advertisements = api_manager.user_service.get_user_advertisements(user_id=user_id)

    await state.set_state(AdvertisementEditingState.start)

    await message.answer(
        f'Выберите объвяление, которое хотите отредактировать: ',
        reply_markup=callback_kb.advertisements_for_update_kb(advertisements=user_advertisements)
    )

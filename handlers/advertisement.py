from aiogram import Router, types, html, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, InputMediaPhoto, CallbackQuery

from keyboards import callback as callback_kb
from keyboards import reply as kb
from services.api import APIManager
from states.custom_states import AdvertisementState

router = Router()
api_manager = APIManager()


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(f'Привет, {html.bold(message.from_user.full_name)}')


@router.message(F.text.lower() == 'создать объявление')
async def start_creating_ad(message: Message, state: FSMContext):
    await state.set_state(AdvertisementState.main_categories)
    await message.answer(f'Выберите один из пунктов ниже', reply_markup=kb.main_categories_kb())


@router.message(AdvertisementState.main_categories)
async def process_main_categories(message: Message, state: FSMContext):
    categories = api_manager.category_service.get_categories()
    await state.update_data(main_categories=message.text)
    await state.set_state(AdvertisementState.property_categories)
    await message.answer(f'Выберите категорию для недвижимости',
                         reply_markup=callback_kb.categories_kb(categories))


@router.callback_query(F.data.contains('category'))
@router.message(AdvertisementState.property_categories)
async def process_photos_qty(callback: CallbackQuery, state: FSMContext):
    _, category_slug = callback.data.split('_')
    category = api_manager.category_service.get_category(category_slug)

    await state.update_data(property_categories=category)
    await state.set_state(AdvertisementState.photos_number)
    await callback.message.answer(f'Выбранная категория: {category["name"]}')
    await callback.message.answer(f'Сколько фотографий добавите для этого объявления?',
                                  reply_markup=ReplyKeyboardRemove())


@router.message(AdvertisementState.photos_number)
async def process_photos_qty(message: Message, state: FSMContext):
    await state.update_data(photo_numbers=int(message.text), photos=[])
    await state.set_state(AdvertisementState.photos)
    await message.answer('Отправьте столько фотографий, сколько указали.')


@router.message(AdvertisementState.photos)
async def process_photos(message: Message, state: FSMContext):
    current_state = await state.get_data()
    current_state['photos'].append(message.photo[-1].file_id)
    if current_state['photo_numbers'] == len(current_state['photos']):
        await state.update_data(photos=current_state['photos'])
        await state.set_state(AdvertisementState.title)
        await message.answer('Напишите заголовок для объявления')


@router.message(AdvertisementState.title)
async def process_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(AdvertisementState.full_description)
    await message.answer('Напишите описание для этого объявления')


@router.message(AdvertisementState.full_description)
async def process_description(message: Message, state: FSMContext):
    districts = api_manager.district_service.get_districts()
    await state.update_data(full_description=message.text)
    await state.set_state(AdvertisementState.district)
    await message.answer('Выберите район, в котором расположена данная недвижимость',
                         reply_markup=callback_kb.districts_kb(districts))


@router.callback_query(F.data.contains('district'))
@router.message(AdvertisementState.district)
async def process_district(callback: CallbackQuery, state: FSMContext):
    _, district_slug = callback.data.split('_')
    district = api_manager.district_service.get_district(district_slug)
    await state.update_data(district=district)
    await state.set_state(AdvertisementState.property_type)
    await callback.message.answer('Выберите тип недвижимости', reply_markup=kb.property_type_kb())


@router.message(AdvertisementState.property_type)
async def process_property(message: Message, state: FSMContext):
    await state.update_data(property_type=message.text)
    await state.set_state(AdvertisementState.price)
    await message.answer('Укажите цену недвижимости', reply_markup=ReplyKeyboardRemove())


@router.message(AdvertisementState.price)
async def process_price(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await state.set_state(AdvertisementState.rooms_from)
    await message.answer('Количество комнат от')


@router.message(AdvertisementState.rooms_from)
async def process_rooms(message: Message, state: FSMContext):
    await state.update_data(rooms_from=message.text)
    await state.set_state(AdvertisementState.rooms_to)
    await message.answer('Количество комнат до')


@router.message(AdvertisementState.rooms_to)
async def process_rooms(message: Message, state: FSMContext):
    await state.update_data(rooms_to=message.text)
    await state.set_state(AdvertisementState.quadrature_from)
    await message.answer('Квадратура от')


@router.message(AdvertisementState.quadrature_from)
async def process_quadrature(message: Message, state: FSMContext):
    await state.update_data(quadrature_from=message.text)
    await state.set_state(AdvertisementState.quadrature_to)
    await message.answer('Квадратура до')


@router.message(AdvertisementState.quadrature_to)
async def process_quadrature(message: Message, state: FSMContext):
    await state.update_data(quadrature_to=message.text)
    await state.set_state(AdvertisementState.floor_from)
    await message.answer('Этаж от')


@router.message(AdvertisementState.floor_from)
async def process_floor(message: Message, state: FSMContext):
    await state.update_data(floor_from=message.text)
    await state.set_state(AdvertisementState.floor_to)
    await message.answer('Этаж до')


@router.message(AdvertisementState.floor_to)
async def process_floor(message: Message, state: FSMContext):
    await state.update_data(floor_to=message.text)
    await state.set_state(AdvertisementState.repair_type)
    await message.answer('Укажите тип ремонта', reply_markup=kb.repair_type_kb())


@router.message(AdvertisementState.repair_type)
async def process_repair(message: Message, state: FSMContext):
    data = await state.get_data()
    title = data.get('title')
    property_category = data.get('property_categories')
    main_category = data.get('main_categories')
    description = data.get('full_description')
    district = data.get('district')
    property_type = data.get('property_type')
    price = data.get('price')
    rooms_from = data.get('rooms_from')
    rooms_to = data.get('rooms_to')
    quadrature_from = data.get('quadrature_from')
    quadrature_to = data.get('quadrature_to')
    floor_from = data.get('floor_from')
    floor_to = data.get('floor_to')
    repair_type = message.text

    msg = f'''
{html.bold('Заголовок: ')}
{html.italic(title)}
{html.bold('Тип объявления: ')}
{html.italic(main_category)}
{html.bold('Описание: ')}
{html.italic(description)}
{html.bold('Район: ')}{html.italic(district['name'])}
{html.bold('Категория недвижимости: ')}{html.italic(property_category['name'])}
{html.bold('Тип недвижимости: ')}{html.italic(property_type)}
{html.bold('Цена: ')}{html.italic(price)}
{html.bold('Кол-во комнат: ')}от {html.italic(rooms_from)} до {html.italic(rooms_to)}
{html.bold('Квадратура: ')}от {html.italic(quadrature_from)} до {html.italic(quadrature_to)}
{html.bold('Этаж: ')}от {html.italic(floor_from)} до {html.italic(floor_to)}
{html.bold('Ремонт: ')}{html.italic(repair_type)}
'''
    media: list[InputMediaPhoto] = [
        InputMediaPhoto(media=img, caption=msg) if i == 0 else InputMediaPhoto(media=img, caption=msg)
        for i, img in enumerate(data['photos'])
    ]

    repair_type_choice = 'with' if repair_type == 'С ремонтом' else 'without'
    property_type_choice = 'new' if property_type == 'Новостройка' else 'old'

    api_manager.advertiser_service.create_advertisement(
        data={
            "name": title,
            "description": description,
            "district": district['id'],
            "property_type": property_type_choice,
            "price": price,
            "rooms_qty_from": rooms_from,
            "rooms_qty_to": rooms_to,
            "quadrature_from": quadrature_from,
            "quadrature_to": quadrature_to,
            "floor_from": floor_from,
            "floor_to": floor_to,
            "auction_allowed": False,
            "category": property_category['id'],
            'repair_type': repair_type_choice,
            "gallery": []
        },
    )

    await message.answer_media_group(media=media)

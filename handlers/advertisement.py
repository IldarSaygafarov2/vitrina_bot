import os
import time

from aiogram import Router, types, html, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder
from filters.realtor import RealtorFilter
from keyboards import callback as callback_kb
from keyboards.callback import return_back_kb, continue_kb
from services.api import api_manager
from templates.advertisements_texts import (
    realtor_welcome_text,
    choose_one_below_text,
    choose_category_text,
    chosen_property_category_text,
    photos_question_text, photos_process_number_text
)

from states.custom_states import AdvertisementState

from settings import BASE_DIR

router = Router(name='advertisement')


@router.message(CommandStart(), RealtorFilter())
async def cmd_start(message: types.Message):
    fullname = message.from_user.full_name
    await message.answer(
        text=realtor_welcome_text(fullname),
        reply_markup=callback_kb.realtor_start_kb()
    )


@router.callback_query(F.data == 'start_realtor')
async def show_realtor_start_menu(
        call: types.CallbackQuery
):
    fullname = call.from_user.full_name
    await call.answer()
    await call.message.edit_text(
        text=realtor_welcome_text(fullname),
        reply_markup=callback_kb.realtor_start_kb()
    )


@router.callback_query(F.data == 'create_ad')
async def process_create_ad(
        call: types.CallbackQuery,
        state: FSMContext
):
    await call.answer()
    await call.message.edit_text(
        text=choose_one_below_text(),
        reply_markup=callback_kb.ads_categories_kb()
    )


@router.callback_query(F.data.startswith('category'))
async def process_category_ad(
        call: types.CallbackQuery,
        state: FSMContext
):
    await call.answer()
    _, operation_type = call.data.split('_')

    await state.update_data(advertisement={'operation_type': operation_type})

    property_categories = api_manager.category_service.get_categories()

    await call.message.edit_text(
        text=choose_category_text(
            operation_type=operation_type
        ),
        reply_markup=callback_kb.property_categories_kb(
            categories=property_categories
        )
    )


@router.callback_query(F.data.startswith('property_category'))
async def process_property_category(
        call: types.CallbackQuery,
        state: FSMContext
):
    await call.answer()
    _, category_slug = call.data.split(':')
    property_category = api_manager.category_service.get_category(category_slug)

    state_data = await state.get_data()
    state_advertisement = state_data.get('advertisement')
    state_advertisement.update({'property_category': property_category})

    await state.update_data(advertisement=state_advertisement)

    msg = chosen_property_category_text(
        category_name=property_category.get('name'),
    ) + photos_question_text()

    await state.set_state(AdvertisementState.photos_number)

    msg = await call.message.edit_text(
        text=msg,
        reply_markup=return_back_kb(
            callback_data=f'category_{state_advertisement["operation_type"]}'
        )
    )
    await state.update_data(adv_message=msg)


@router.message(AdvertisementState.photos_number)
async def get_advertisement_photos_number(
        message: types.Message,
        state: FSMContext
):
    photos_number = int(message.text)

    state_data = await state.get_data()
    advertisement_state = state_data.get('advertisement')
    await state.update_data(
        advertisement=advertisement_state,
        photos=[],
        message_ids=[],
        photos_number=photos_number,

    )

    adv_message = state_data.get('adv_message')

    await state.set_state(AdvertisementState.photos)

    callback_for_kb = f'property_category:{advertisement_state["property_category"]["slug"]}'
    msg = await adv_message.edit_text(
        text=photos_process_number_text(photos_number=photos_number),
        reply_markup=return_back_kb(
            callback_data=callback_for_kb
        )
    )
    await state.update_data(adv_message=msg)
    await message.delete()


@router.message(AdvertisementState.photos)
async def get_advertisement_photos(
        message: types.Message,
        state: FSMContext
):
    state_data = await state.get_data()
    photos: list = state_data.get('photos')
    photos_number = state_data.get('photos_number')
    message_ids = state_data.get('message_ids')

    photo_file_id = message.photo[-1].file_id

    photos.append(photo_file_id)

    if len(photos) == photos_number:
        media_group = MediaGroupBuilder()

        for idx, photo in enumerate(photos):
            file = await message.bot.get_file(file_id=photo)
            file_path = file.file_path
            file_name = file_path.split('/')[-1]
            if not os.path.exists(BASE_DIR / 'media'):
                os.makedirs(BASE_DIR / 'photos', exist_ok=True)
            await message.bot.download_file(file_path, f'photos/{file_name}')

            media_group.add_photo(
                media=FSInputFile(path=file_path),
                caption='Продолжить' if idx == 0 else None,
                reply_markup=continue_kb()
            )

        message_ids.append(message_ids[-1] + 1)

        for message_id in message_ids:
            await message.bot.delete_message(
                chat_id=message.chat.id,
                message_id=message_id
            )
        await message.answer_media_group(
            media=media_group.build(),
            reply_markup=continue_kb()
        )

        # time.sleep(1)
        #
        # await message.edit_media(
        #     media=media_group.build(),
        #     reply_markup=continue_kb()
        # )
    else:
        message_ids.append(message.message_id)

        # await state.update_data(photos=photos)
        # await state.set_state(AdvertisementState.title)

    # if photos_number != len(state_data['photos']):
    #     await adv_message.edit_text(
    #         text=f'Осталось отправить: <b>{photos_number - photos_len} фотографий</b>',
    #         reply_markup=return_back_kb(callback_for_kb)
    #     )
    # else:
    #
    #     await state.update_data(photos=state_data['photos'])
    #     await state.set_state(AdvertisementState.title)

#
# @router.message(F.text.lower() == 'создать объявление')
# async def start_creating_ad(message: Message, state: FSMContext):
#     await state.set_state(AdvertisementState.main_categories)
#     await message.answer(
#         choose_one_below_text(),
#         reply_markup=kb.main_categories_kb()
#     )
#
#

#
#
# @router.message(AdvertisementState.main_categories)
# async def process_main_categories(message: Message, state: FSMContext):
#     categories = api_manager.category_service.get_categories()
#     await state.update_data(main_categories=message.text)
#     await state.set_state(AdvertisementState.property_categories)
#     await message.answer(
#         choose_category_text(),
#         reply_markup=callback_kb.categories_kb(categories)
#     )
#
#
# @router.callback_query(F.data.contains('category'))
# @router.message(AdvertisementState.property_categories)
# async def process_photos_qty(callback: CallbackQuery, state: FSMContext):
#     _, category_slug = callback.data.split('_')
#     category = api_manager.category_service.get_category(category_slug)
#
#     await state.update_data(property_categories=category)
#     await state.set_state(AdvertisementState.photos_number)
#     await callback.message.answer(f'Выбранная категория: {html.bold(category["name"])}')
#     await callback.message.answer(f'Сколько фотографий добавите для этого объявления?',
#                                   reply_markup=ReplyKeyboardRemove())
#
#
# @router.message(AdvertisementState.photos_number)
# async def process_photos_qty(message: Message, state: FSMContext):
#     await state.update_data(photo_numbers=int(message.text), photos=[])
#     await state.set_state(AdvertisementState.photos)
#     await message.answer('Отправьте столько фотографий, сколько указали: ')
#
#
# @router.message(AdvertisementState.photos)
# async def process_photos(message: Message, state: FSMContext):
#     current_state = await state.get_data()
#     current_state['photos'].append(message.photo[-1].file_id)
#     if current_state['photo_numbers'] == len(current_state['photos']):
#         await state.update_data(photos=current_state['photos'])
#         await state.set_state(AdvertisementState.title)
#         await message.answer('Напишите заголовок для объявления: ')
#
#
# @router.message(AdvertisementState.title)
# async def process_title(message: Message, state: FSMContext):
#     await state.update_data(title=message.text)
#     await state.set_state(AdvertisementState.full_description)
#     await message.answer('Напишите описание для этого объявления: ')
#
#
# @router.message(AdvertisementState.full_description)
# async def process_description(message: Message, state: FSMContext):
#     districts = api_manager.district_service.get_districts()
#     await state.update_data(full_description=message.text)
#     await state.set_state(AdvertisementState.district)
#     await message.answer('Выберите район, в котором расположена данная недвижимость: ',
#                          reply_markup=callback_kb.districts_kb(districts))
#
#
# @router.callback_query(F.data.contains('district'))
# @router.message(AdvertisementState.district)
# async def process_district(callback: CallbackQuery, state: FSMContext):
#     _, district_slug = callback.data.split('_')
#     data = await state.get_data()
#     district = api_manager.district_service.get_district(district_slug)
#     await state.update_data(district=district)
#     await callback.message.answer(f'Выбранный район: {html.bold(district["name"])}')
#
#     property_data = data['property_categories']['slug']
#     if property_data == 'doma':
#         await state.set_state(AdvertisementState.house_quadrature)
#         await callback.message.answer('Укажите общую площадь участка')
#     else:
#         await state.set_state(AdvertisementState.address)
#         await callback.message.answer('Напишите точный адрес недвижимости')
#
#
# @router.message(AdvertisementState.house_quadrature)
# async def process_house_quadrature(message: Message, state: FSMContext):
#     data = await state.get_data()
#     await state.update_data(house_quadrature=int(message.text))
#     await state.set_state(AdvertisementState.address)
#     await message.answer('Напишите точный адрес недвижимости')
#
#
# @router.message(AdvertisementState.address)
# async def process_address(message: Message, state: FSMContext):
#     await state.update_data(address=message.text)
#     await state.set_state(AdvertisementState.property_type)
#     await message.answer('Выберите тип недвижимости: ', reply_markup=kb.property_type_kb())
#
#
# @router.message(AdvertisementState.property_type)
# async def process_property(message: Message, state: FSMContext):
#     await state.update_data(property_type=message.text)
#     if message.text == 'Новостройка':
#         await state.set_state(AdvertisementState.creation_date)
#         await message.answer('Укажите год постройки новостройки')
#     elif message.text == 'Вторичный фонд':
#         await state.set_state(AdvertisementState.price)
#         await state.update_data(creation_date=0)
#         await message.answer('Укажите цену недвижимости: ', reply_markup=ReplyKeyboardRemove())
#
#
# @router.message(AdvertisementState.creation_date)
# async def process_creation_date(message: Message, state: FSMContext):
#     await state.update_data(creation_date=message.text)
#     await state.set_state(AdvertisementState.price)
#     await message.answer('Укажите цену недвижимости', reply_markup=ReplyKeyboardRemove())
#
#
# @router.message(AdvertisementState.price)
# async def process_price(message: Message, state: FSMContext):
#     await state.update_data(price=message.text)
#     await state.set_state(AdvertisementState.auction_allowed)
#     await message.answer('Уместен ли торг?', reply_markup=kb.is_auction_allowed_kb())
#
#
# @router.message(AdvertisementState.auction_allowed)
# async def process_auction_allowed(message: Message, state: FSMContext):
#     is_allowed = True if message.text == 'Да' else False
#     await state.update_data(auction_allowed=is_allowed)
#     await state.set_state(AdvertisementState.is_studio)
#     await message.answer('Квартира является студией?', reply_markup=kb.is_studio_kb())
#
#
# @router.message(AdvertisementState.is_studio)
# async def process_is_studio(message: Message, state: FSMContext):
#     if message.text == 'Да':
#         await state.update_data(is_studio=True)
#         await state.set_state(AdvertisementState.quadrature_from)
#         await message.answer('Укажите квадратуру: ')
#     else:
#         await state.update_data(is_studio=False)
#         await state.set_state(AdvertisementState.rooms_from)
#         await message.answer('Количество комнат от: ')
#
#
# @router.message(AdvertisementState.rooms_from)
# async def process_rooms(message: Message, state: FSMContext):
#     await state.update_data(rooms_from=message.text)
#     await state.set_state(AdvertisementState.rooms_to)
#     await message.answer('Количество комнат до: ')
#
#
# @router.message(AdvertisementState.rooms_to)
# async def process_rooms(message: Message, state: FSMContext):
#     await state.update_data(rooms_to=message.text)
#     await state.set_state(AdvertisementState.quadrature_from)
#     await message.answer('Квадратура от: ')
#
#
# @router.message(AdvertisementState.quadrature_from)
# async def process_quadrature(message: Message, state: FSMContext):
#     await state.update_data(quadrature_from=message.text)
#     await state.set_state(AdvertisementState.quadrature_to)
#     await message.answer('Квадратура до: ')
#
#
# @router.message(AdvertisementState.quadrature_to)
# async def process_quadrature(message: Message, state: FSMContext):
#     await state.update_data(quadrature_to=message.text)
#     await state.set_state(AdvertisementState.floor_from)
#     await message.answer('Этаж от: ')
#
#
# @router.message(AdvertisementState.floor_from)
# async def process_floor(message: Message, state: FSMContext):
#     await state.update_data(floor_from=message.text)
#     await state.set_state(AdvertisementState.floor_to)
#     await message.answer('Этаж до: ')
#
#
# @router.message(AdvertisementState.floor_to)
# async def process_floor(message: Message, state: FSMContext):
#     await state.update_data(floor_to=message.text)
#     await state.set_state(AdvertisementState.repair_type)
#     await message.answer('Укажите тип ремонта: ', reply_markup=kb.repair_type_kb())
#
#
# @router.message(AdvertisementState.repair_type)
# async def process_repair(message: Message, state: FSMContext):
#     data = await state.get_data()
#     title = data.get('title')
#     is_allowed = data.get('auction_allowed')
#     property_category = data.get('property_categories')
#     main_category = data.get('main_categories')
#     description = data.get('full_description')
#     district = data.get('district')
#     property_type = data.get('property_type')
#     price = data.get('price')
#     rooms_from = data.get('rooms_from', 0)
#     rooms_to = data.get('rooms_to', 0)
#     quadrature_from = data.get('quadrature_from')
#     quadrature_to = data.get('quadrature_to')
#     floor_from = data.get('floor_from')
#     floor_to = data.get('floor_to')
#     repair_type = message.text
#     is_studio = data.get('is_studio')
#     creation_date = data.get('creation_date')
#     address = data.get('address')
#     house_quadrature = data.get('house_quadrature')
#     # msg = create_advertisement_message(data)
#     file_names = []
#
#     for photo in data['photos']:
#         file = await bot.get_file(photo)
#         file_path = file.file_path
#         file_names.append(file_path.split('/')[-1])
#         await bot.download_file(file_path, f'media/{file_path.split("/")[-1]}')
#
#     repair_type_choice = get_repair_type_by_name(repair_type)
#     property_type_choice = get_property_type(property_type)
#
#     username = message.from_user.username
#     user_id = api_manager.user_service.get_user_id(username)
#     print(user_id)
#
#     t = f'{html.bold('Кол-во комнат: ')}от {html.italic(rooms_from)} до {html.italic(rooms_to)}'
#     t2 = f'\n{html.bold("Год постройки: ")}{html.italic(creation_date)}' if creation_date else ''
#     t3 = f'\n<b>Общая площадь участка: </b><i>{house_quadrature}</i>' if property_category['slug'] == 'doma' else ''
#
#     msg = f'''
# {html.bold('Заголовок: ')}
# {html.italic(title)}
# {html.bold('Тип объявления: ')}
# {html.italic(main_category)}
# {html.bold('Описание: ')}
# {html.italic(description)}
# {html.bold('Район: ')}{html.italic(district['name'])}
# {html.bold('Адрес: ')}{html.italic(address)}
# {html.bold('Категория недвижимости: ')}{html.italic(property_category['name'])}
# {html.bold('Тип недвижимости: ')}{html.italic(property_type)}{t2}
# {html.bold('Цена: ')}{html.italic(price)}{t3}
# {t if not is_studio else f'{html.bold("Кол-во комнат: ")} Студия'}
# {html.bold('Квадратура: ')}от {html.italic(quadrature_from)} до {html.italic(quadrature_to)}
# {html.bold('Этаж: ')}от {html.italic(floor_from)} до {html.italic(floor_to)}
# {html.bold('Ремонт: ')}{html.italic(repair_type)}
# '''
#
#     media: list[InputMediaPhoto] = [
#         InputMediaPhoto(media=img, caption=msg) if i == 0 else InputMediaPhoto(media=img, caption=msg)
#         for i, img in enumerate(data['photos'])
#     ]
#
#     new = api_manager.advertiser_service.create_advertisement(
#         data={
#             "name": title,
#             "description": description,
#             "district": district['id'],
#             "address": address,
#             "property_type": property_type_choice,
#             "price": price,
#             "rooms_qty_from": rooms_from,
#             "rooms_qty_to": rooms_to,
#             "quadrature_from": quadrature_from,
#             "quadrature_to": quadrature_to,
#             "floor_from": floor_from,
#             "floor_to": floor_to,
#             "auction_allowed": is_allowed,
#             "category": property_category['id'],
#             'repair_type': repair_type_choice,
#             'house_quadrature': house_quadrature,
#             'is_studio': is_studio,
#             'user': user_id['id'],
#         },
#     )
#
#     media_files = os.listdir('media')
#     for media_file in media_files:
#         if media_file not in file_names:
#             continue
#
#         file = open(f'media/{media_file}', 'rb')
#         media_data = {'photo': file}
#         data = {'advertisement': new['id']}
#         res = api_manager.advertiser_service.upload_image_to_gallery(
#             advertisement_id=new['id'],
#             files=media_data,
#             data=data
#         )
#         print(res)
#
#     await message.answer_media_group(media=media)
#     await state.clear()
#     await message.answer('Выберите действие ниже', reply_markup=kb.start_kb())


# @router.message(F.text.lower() == 'мои объявления')
# async def realtors_advertisements(message: Message, state: FSMContext):
#     await message.answer(
#         choose_one_below_text(),
#         reply_markup=kb.ad_moderated_kb()
#     )
#
#
# @router.message(F.text.lower() == 'проверенные')
# async def realtors_moderated_ads(message: Message, state: FSMContext):
#     username = message.from_user.username
#     user_id = api_manager.user_service.get_user_id(username)
#     advertisements = api_manager.user_service.get_user_advertisements(
#         user_id=user_id['id'],
#         params={'is_moderated': True}
#     )
#     msg = total_checked_or_unchecked_advertisements_text(advertisements, is_checked=True)
#     await message.answer(msg)
#     for advertisement in advertisements:
#         adv_msg = create_advertisement_message(advertisement)
#         await message.answer(adv_msg)
#
#
# @router.message(F.text.lower() == 'непроверенные')
# async def realtors_moderated_ads(message: Message, state: FSMContext):
#     username = message.from_user.username
#     user_id = api_manager.user_service.get_user_id(username)
#     advertisements = api_manager.user_service.get_user_advertisements(
#         user_id=user_id['id'],
#         params={'is_moderated': False}
#     )
#     msg = total_checked_or_unchecked_advertisements_text(advertisements, is_checked=False)
#     await message.answer(msg)
#     for advertisement in advertisements:
#         adv_msg = create_advertisement_message(advertisement)
#         await message.answer(adv_msg)

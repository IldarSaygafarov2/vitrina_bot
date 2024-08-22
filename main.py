import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, InputMediaPhoto

import api
import settings
from custom_states import AdvertisementState
from keyboards import reply as kb

dp = Dispatcher()


@dp.message(CommandStart(), F.chat.func(lambda chat: api.is_user_realtor(chat.username)))
async def start(message: Message):
    await message.answer(f'Hello, {html.bold(message.from_user.full_name)}', reply_markup=kb.start_kb())


@dp.message(F.text.lower() == 'создать объявление')
async def start_creating_ad(message: Message, state: FSMContext):
    await state.set_state(AdvertisementState.main_categories)
    await message.answer(f'Выберите один из пунктов ниже', reply_markup=kb.main_categories_kb())


@dp.message(AdvertisementState.main_categories)
async def process_main_categories(message: Message, state: FSMContext):
    await state.update_data(main_categories=message.text)
    await state.set_state(AdvertisementState.property_categories)
    await message.answer(f'Выберите категорию для недвижимости', reply_markup=kb.property_categories_kb())


@dp.message(AdvertisementState.property_categories)
async def process_photos_qty(message: Message, state: FSMContext):
    await state.update_data(main_categories=message.text)
    await state.set_state(AdvertisementState.photos_number)
    await message.answer(f'Сколько фотографий добавите для этого объявления?',
                         reply_markup=ReplyKeyboardRemove())


@dp.message(AdvertisementState.photos_number)
async def process_photos_qty(message: Message, state: FSMContext):
    await state.update_data(photo_numbers=int(message.text), photos=[])

    await state.set_state(AdvertisementState.photos)
    await message.answer('Отправьте столько фотографий, сколько указали.')


@dp.message(AdvertisementState.photos)
async def process_photos(message: Message, state: FSMContext):
    current_state = await state.get_data()
    current_state['photos'].append(message.photo[-1].file_id)
    if current_state['photo_numbers'] == len(current_state['photos']):
        await state.update_data(photos=current_state['photos'])
        await state.set_state(AdvertisementState.title)
        await message.answer('Напишите заголовок для объявления')


@dp.message(AdvertisementState.title)
async def process_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(AdvertisementState.full_description)
    await message.answer('Напишите описание для этого объявления')


@dp.message(AdvertisementState.full_description)
async def process_description(message: Message, state: FSMContext):
    await state.update_data(full_description=message.text)
    await state.set_state(AdvertisementState.district)
    await message.answer('Выберите район, в котором расположена данная недвижимость', reply_markup=kb.districts_kb())


@dp.message(AdvertisementState.district)
async def process_district(message: Message, state: FSMContext):
    await state.update_data(district=message.text)
    await state.set_state(AdvertisementState.property_type)
    await message.answer('Выберите тип недвижимости', reply_markup=kb.property_type_kb())


@dp.message(AdvertisementState.property_type)
async def process_property(message: Message, state: FSMContext):
    await state.update_data(property_type=message.text)
    await state.set_state(AdvertisementState.price)
    await message.answer('Укажите цену недвижимости', reply_markup=ReplyKeyboardRemove())


@dp.message(AdvertisementState.price)
async def process_price(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await state.set_state(AdvertisementState.rooms_from)
    await message.answer('Количество комнат от')


@dp.message(AdvertisementState.rooms_from)
async def process_rooms(message: Message, state: FSMContext):
    await state.update_data(rooms_from=message.text)
    await state.set_state(AdvertisementState.rooms_to)
    await message.answer('Количество комнат до')


@dp.message(AdvertisementState.rooms_to)
async def process_rooms(message: Message, state: FSMContext):
    await state.update_data(rooms_to=message.text)
    await state.set_state(AdvertisementState.quadrature_from)
    await message.answer('Квадратура от')


@dp.message(AdvertisementState.quadrature_from)
async def process_quadrature(message: Message, state: FSMContext):
    await state.update_data(quadrature_from=message.text)
    await state.set_state(AdvertisementState.quadrature_to)
    await message.answer('Квадратура до')


@dp.message(AdvertisementState.quadrature_to)
async def process_quadrature(message: Message, state: FSMContext):
    await state.update_data(quadrature_to=message.text)
    await state.set_state(AdvertisementState.floor_from)
    await message.answer('Этаж от')


@dp.message(AdvertisementState.floor_from)
async def process_floor(message: Message, state: FSMContext):
    await state.update_data(floor_from=message.text)
    await state.set_state(AdvertisementState.floor_to)
    await message.answer('Этаж до')


@dp.message(AdvertisementState.floor_to)
async def process_floor(message: Message, state: FSMContext):
    await state.update_data(floor_to=message.text)
    await state.set_state(AdvertisementState.repair_type)
    await message.answer('Укажите тип ремонта', reply_markup=kb.repair_type_kb())


@dp.message(AdvertisementState.repair_type)
async def process_repair(message: Message, state: FSMContext):
    data = await state.get_data()
    msg = f'''
{html.bold('Заголовок: ')}
{html.italic(data['title'])}
{html.bold('Тип объявления: ')}
{html.italic(data['main_categories'])}
{html.bold('Описание: ')}
{html.italic(data['full_description'])}
{html.bold('Район: ')}{html.italic(data['district'])}
{html.bold('Тип недвижимости: ')}{html.italic(data['property_type'])}
{html.bold('Цена: ')}{html.italic(data['price'])}
{html.bold('Кол-во комнат от: ')}{html.italic(data['rooms_from'])}
{html.bold('Кол-во комнат до: ')}{html.italic(data['rooms_to'])}
{html.bold('Квадратура от: ')}{html.italic(data['quadrature_from'])}
{html.bold('Квадратура до: ')}{html.italic(data['quadrature_to'])}
{html.bold('Этаж от: ')}{html.italic(data['floor_from'])}
{html.bold('Этаж до: ')}{html.italic(data['floor_to'])}
{html.bold('Ремонт: ')}{html.italic(message.text)}
'''
    media = [InputMediaPhoto(media=i) for i in data['photos']]
    await message.answer_media_group(media=media)
    await message.answer(msg)


async def main():
    bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

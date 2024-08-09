import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, InputMediaPhoto
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton, ReplyKeyboardMarkup

import settings
from custom_states import AdvertisementState

dp = Dispatcher()


def start_kb():
    reply_builder = ReplyKeyboardBuilder()
    reply_builder.add(
        KeyboardButton(text='Создать объявление')
    )
    return reply_builder.as_markup()


districts_list = [
    'Алмазарский район',
    'Бектемирский район',
    'Мирабадский район',
    'Мирзо-Улугбекский район',
    'Сергелийский район',
    'Учтепинский район',
    'Чиланзарский район',
    'Шайхантахурский район',
    'Юнусабадский район',
    'Яккасарайский район',
    'Яшнабадский район'
]


def districts_kb():
    reply_builder = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text=district)] for district in districts_list
        ])
    return reply_builder


def property_type_kb():
    reply_builder = ReplyKeyboardBuilder()
    reply_builder.add(
        KeyboardButton(text='Новостройка'),
        KeyboardButton(text='Вторичный фонд')
    )
    return reply_builder.as_markup()


def repair_type_kb():
    reply_builder = ReplyKeyboardBuilder()
    reply_builder.add(
        KeyboardButton(text='С ремонтом'),
        KeyboardButton(text='Коробка без ремонта')
    )
    return reply_builder.as_markup()


@dp.message(CommandStart())
async def start(message: Message):
    # db.create_user(chat_id=message.chat.id)
    await message.answer(f'Hello, {html.bold(message.from_user.full_name)}', reply_markup=start_kb())


@dp.message(F.text.lower() == 'создать объявление')
async def start_creating_ad(message: Message, state: FSMContext):
    await state.set_state(AdvertisementState.photos_number)
    await message.answer(f'Сколько фотографий добавите для этого объявления?',
                         reply_markup=ReplyKeyboardRemove())


@dp.message(AdvertisementState.photos_number)
async def process_photos_qty(message: Message, state: FSMContext):
    chat_id = message.chat.id
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
    await message.answer('Выберите район, в котором расположена данная недвижимость', reply_markup=districts_kb())


@dp.message(AdvertisementState.district)
async def process_district(message: Message, state: FSMContext):
    await state.update_data(district=message.text)
    await state.set_state(AdvertisementState.property_type)
    await message.answer('Выберите тип недвижимости', reply_markup=property_type_kb())


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
    await message.answer('Укажите тип ремонта', reply_markup=repair_type_kb())


@dp.message(AdvertisementState.repair_type)
async def process_repair(message: Message, state: FSMContext):
    data = await state.get_data()
    msg = f'''
{html.bold('Заголовок: ')}
{data['title']}
{html.bold('Описание: ')}
{data['full_description']}
{html.bold('Район: ')} {data['district']}
{html.bold('Тип недвижимости: ')}{data['property_type']}
{html.bold('Цена: ')}{data['price']}
{html.bold('Кол-во комнат от: ')}{data['rooms_from']}
{html.bold('Кол-во комнат до: ')}{data['rooms_to']}
{html.bold('Квадратура от: ')}{data['quadrature_from']}
{html.bold('Квадратура до: ')}{data['quadrature_to']}
{html.bold('Этаж от: ')}{data['floor_from']}
{html.bold('Этаж до: ')}{data['floor_to']}
{html.bold('Ремонт: ')}{message.text}
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

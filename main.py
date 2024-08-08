import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton
from custom_states import AdvertisementState
import settings
from aiogram.fsm.context import FSMContext
import db

dp = Dispatcher()


def start_kb():
    reply_builder = ReplyKeyboardBuilder()
    reply_builder.add(
        KeyboardButton(text='Создать объявление')
    )
    return reply_builder.as_markup()


@dp.message(CommandStart())
async def start(message: Message):
    db.create_user(chat_id=message.chat.id)
    await message.answer(f'Hello, {html.bold(message.from_user.full_name)}', reply_markup=start_kb())


@dp.message(F.text.lower() == 'создать объявление')
async def start_creating_ad(message: Message, state: FSMContext):
    # chat_id = message.chat.id
    await state.set_state(AdvertisementState.photos)

    await message.answer(f'Отправьте фотографии для этого объявления',
                         reply_markup=ReplyKeyboardRemove())


@dp.message(AdvertisementState.photos)
async def process_photos(message: Message, state: FSMContext):
    user_id = db.get_user_id(message.chat.id)
    db.create_photo_path(user_id, message.photo[-1].file_id)

    await state.update_data()
    await message.answer('Добавили фото')




async def main():
    bot = Bot(token=settings.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

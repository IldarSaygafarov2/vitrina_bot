from aiogram import types, Router
from aiogram.filters import Command

router = Router(name='simple_user')


@router.message(Command(commands=['start']))
async def simple_user(message: types.Message):
    await message.answer(f'Hello simple user')
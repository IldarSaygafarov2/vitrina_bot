from aiogram import types, Router
from aiogram.filters import CommandStart

router = Router(name='simple_user')


@router.message(CommandStart())
async def simple_user_start(message: types.Message):
    await message.answer(f'Добро пожаловать в бот Vitrina')

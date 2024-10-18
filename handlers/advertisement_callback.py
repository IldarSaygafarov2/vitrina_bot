# from aiogram import Router, F
# from aiogram.filters import CommandStart
# from aiogram.fsm.context import FSMContext
# from aiogram.types import (
#     Message,
#     CallbackQuery
# )
#
# from filters.realtor import RealtorFilter
# from keyboards.advertisement_callback import (
#     callback_advertisement_start_kb,
#     callback_operation_types_kb
# )
#
# advertisement_callback_router = Router()
#
#
# @advertisement_callback_router.message(
#     CommandStart(),
#     RealtorFilter()
# )
# async def realtor_advertisement_start(
#         message: Message
# ):
#     username = message.from_user.username
#     await message.answer(
#         text=f'Добро пожаловать, <b>{username}</b>\n\n'
#              f'Выберите действие ниже ⬇',
#         reply_markup=callback_advertisement_start_kb()
#     )
#
#
# @advertisement_callback_router.callback_query(
#     F.data == 'callback_advertisement_create'
# )
# async def callback_advertisement_create(
#         call: CallbackQuery,
#         state: FSMContext
# ):
#     await call.answer()
#
#     await call.message.edit_text(
#         text='Выберите тип операции для данного объявления',
#         reply_markup=callback_operation_types_kb()
#     )
#
#
#
# @advertisement_callback_router.callback_query(
#     F.data == 'callback_advertisements_list'
# )
# async def callback_advertisements_list(
#         call: CallbackQuery,
#         state: FSMContext
# ):
#     await call.answer()
#
#
#
# # callback_advertisement_create
# # callback_advertisements_list
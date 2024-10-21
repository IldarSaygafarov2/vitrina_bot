from statistics import pvariance
from typing import Optional

from aiogram.utils.keyboard import InlineKeyboardBuilder

from settings import OPERATION_TYPES


def callback_advertisement_start_kb():
    kb = InlineKeyboardBuilder()

    kb.button(text='Создать объявление', callback_data='callback_advertisement_create')
    kb.button(text='Мои объявления', callback_data='callback_advertisements_list')

    kb.adjust(2)

    return kb.as_markup()


def callback_operation_types_kb():
    kb = InlineKeyboardBuilder()
    for key, value in OPERATION_TYPES.items():
        kb.button(text=value, callback_data=f'callback_operation_type:{key}')

    kb.button(text='Назад', callback_data='callback_return_back')

    kb.adjust(2)
    return kb.as_markup()

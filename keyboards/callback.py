from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def districts_kb(districts: list) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=district['name'], callback_data=f'district_{district["slug"]}')
            ] for district in districts
        ]
    )
    return kb


def categories_kb(categories: list) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=category["name"], callback_data=f'category_{category["slug"]}')]
            for category in categories
        ]
    )
    return kb


def realtors_kb(realtors_list: list):
    kb = InlineKeyboardBuilder()
    for realtor in realtors_list:
        kb.button(text=f'{realtor["first_name"]} {realtor["last_name"]}',
                  callback_data=f'realtor_{realtor["tg_username"]}_{realtor["id"]}')

    kb.adjust(2, 2)
    return kb.as_markup()




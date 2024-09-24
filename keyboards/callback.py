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
                  callback_data=f'realtor-{realtor["tg_username"]}-{realtor["id"]}')

    kb.adjust(2, 2)
    return kb.as_markup()


def moderate_adv_kb(adv_id: int):
    kb = InlineKeyboardBuilder()
    kb.button(text='✅', callback_data=f'yes_{adv_id}')
    kb.button(text='🚫', callback_data=f'no_{adv_id}')
    kb.adjust(2, 2)
    return kb.as_markup()

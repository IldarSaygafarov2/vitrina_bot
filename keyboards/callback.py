from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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

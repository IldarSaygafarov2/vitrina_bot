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

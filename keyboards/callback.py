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
                  callback_data=f'realtor:{realtor["tg_username"]}:{realtor["id"]}')
    kb.button(text='Назад', callback_data='start_menu')
    kb.adjust(2)
    return kb.as_markup()


def group_director_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text='Список риелторов', callback_data='realtors_list')
    kb.button(text='Последние объявления', callback_data='latest_ads')

    kb.adjust(2)
    return kb.as_markup()


def ads_moderation_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text='Проверенные', callback_data='checked_ads')
    kb.button(text='Непроверенные', callback_data='unchecked_ads')
    kb.button(text='Назад', callback_data='realtors_list')
    kb.adjust(2)
    return kb.as_markup()


def moderate_adv_kb(adv_id: int):
    kb = InlineKeyboardBuilder()
    kb.button(text='✅', callback_data=f'yes_{adv_id}')
    kb.button(text='🚫', callback_data=f'no_{adv_id}')
    kb.adjust(2, 2)
    return kb.as_markup()


def realtor_advertisements_kb(ads_list: list, checked: bool):
    kb = InlineKeyboardBuilder()
    for idx, ad in enumerate(ads_list, start=1):
        callback_data = f'checked_ad:{ad["id"]}' if checked else f'unchecked_ad:{ad["id"]}'
        kb.button(text=f'{idx}. {ad["name"]}', callback_data=callback_data)
    kb.adjust(1)
    kb.row(
        InlineKeyboardButton(text='Назад', callback_data='realtors_list')
    )
    return kb.as_markup()


def return_to_ads_kb(callback_data: str, adv_id: int, show_checks: bool = True):
    kb = InlineKeyboardBuilder()
    if show_checks:
        kb.button(text='✅', callback_data=f'yes_{adv_id}')
        kb.button(text='🚫', callback_data=f'no_{adv_id}')
    kb.button(text='Назад', callback_data=callback_data)
    kb.adjust(2)
    return kb.as_markup()

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from settings import KB_FIELDS, OPERATION_TYPES, REPAIR_TYPES, PROPERTY_TYPES


def realtor_start_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text='Мои объявления', callback_data='show_my_ads')
    kb.button(text='Добавить объявление', callback_data='create_ad')
    kb.adjust(2)
    return kb.as_markup()


def ads_categories_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text='Аренда', callback_data='category_Аренда')
    kb.button(text='Покупка', callback_data='category_Покупка')
    kb.button(text='Назад', callback_data='start_realtor')
    kb.adjust(2)
    return kb.as_markup()


def group_director_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text='Список риелторов', callback_data='realtors_list')
    kb.button(text='Последние объявления', callback_data='latest_ads')

    kb.adjust(2)
    return kb.as_markup()


def districts_kb(districts: list, callback_data: str | None = None) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for district in districts:
        kb.button(text=district['name'], callback_data=f'district_{district["slug"]}')
    kb.adjust(1)
    if callback_data is not None:
        kb.row(InlineKeyboardButton(text='Назад', callback_data=callback_data))
    return kb.as_markup()


def property_categories_kb(
        categories: list,
        callback_data: str | None = None,
        additional_callback: str = ''
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for category in categories:
        kb.button(
            text=category.get('name'),
            callback_data=f'{additional_callback}property_category:{category["slug"]}'
        )
    kb.adjust(2)
    if callback_data is not None:
        kb.row(InlineKeyboardButton(text='Назад', callback_data=callback_data))
    return kb.as_markup()


def realtors_kb(realtors_list: list):
    kb = InlineKeyboardBuilder()
    for realtor in realtors_list:
        kb.button(text=f'{realtor["first_name"]} {realtor["last_name"]}',
                  callback_data=f'realtor:{realtor["tg_username"]}:{realtor["id"]}')
    kb.button(text='Назад', callback_data='start_menu')
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


def return_back_kb(callback_data: str):
    kb = InlineKeyboardBuilder()
    kb.button(text='Назад', callback_data=callback_data)
    return kb.as_markup()


def continue_kb():
    kb = InlineKeyboardBuilder()
    kb.button(text='Продолжить', callback_data='continue')
    return kb.as_markup()


def realtors_ads_kb(realtor_id: int):
    kb = InlineKeyboardBuilder()
    kb.button(text='Проверенные', callback_data=f'checked_ads:{realtor_id}')
    kb.button(text='Непроверенные', callback_data=f'unchecked_ads:{realtor_id}')
    kb.adjust()
    return kb.as_markup()


def advertisements_for_update_kb(advertisements: list):
    kb = InlineKeyboardBuilder()
    for idx, advertisement in enumerate(advertisements, start=1):
        advertisement_name = advertisement.get('name')
        advertisement_name = f'{idx}. {advertisement_name}' if advertisement_name else f'Обявление №{idx}'
        kb.button(
            text=advertisement_name,
            callback_data=f'advertisement_update:{advertisement["id"]}'
        )
    kb.adjust(1)
    kb.row(
        InlineKeyboardButton(text='На главную', callback_data='realtor_start_menu')
    )
    return kb.as_markup()


def advertisement_fields_for_update_kb(adv_id: int):
    kb = InlineKeyboardBuilder()
    for call, field in KB_FIELDS.items():
        kb.button(text=field, callback_data=f'field_update:{adv_id}:{call}')
    kb.adjust(2)
    kb.row(
        InlineKeyboardButton(text='Назад', callback_data='back_to_ads')
    )
    return kb.as_markup()


def advertisement_choices_kb(choice_type: str, callback_for_return: str | None = None, **kwargs):
    kb = InlineKeyboardBuilder()

    prefix = 'update_'

    if choice_type == 'repair_type':
        for key, value in REPAIR_TYPES.items():
            kb.button(text=value, callback_data=f'{prefix}{choice_type}:{key}')
    elif choice_type == 'property_type':
        for key, value in PROPERTY_TYPES.items():
            kb.button(text=value, callback_data=f'{prefix}{choice_type}:{key}')
    elif choice_type == 'operation_type':
        for key, value in OPERATION_TYPES.items():
            kb.button(text=value, callback_data=f'{prefix}{choice_type}:{key}')

    kb.adjust(2)
    if callback_for_return is not None:
        kb.row(InlineKeyboardButton(text='Назад', callback_data=callback_for_return))

    return kb.as_markup()


def advertisement_is_studio_kb(callback_data_for_return: str):
    kb = InlineKeyboardBuilder()
    kb.button(text='Да', callback_data='studio_yes')
    kb.button(text='Нет', callback_data='studio_no')

    kb.button(text='Назад', callback_data=callback_data_for_return)
    kb.adjust(2)
    return kb.as_markup()


def gallery_update_kb(gallery: list[dict[str, str | int]], callback_data_for_return: str = None):
    kb = InlineKeyboardBuilder()
    for idx, obj in enumerate(gallery, start=1):
        kb.button(text=str(idx), callback_data=f'gallery_update:{obj["id"]}')
    kb.adjust(2)
    if callback_data_for_return is not None:
        kb.row(InlineKeyboardButton(text='Назад', callback_data=callback_data_for_return))
    return kb.as_markup()

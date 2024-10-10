from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


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


def districts_kb(districts: list) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=district['name'], callback_data=f'district_{district["slug"]}')
            ] for district in districts
        ]
    )
    return kb


def property_categories_kb(categories: list) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for category in categories:
        kb.button(text=category.get('name'), callback_data=f'property_category:{category["slug"]}')
    kb.adjust(2)
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


def process_update_advertisement_kb(adv_id: int):
    kb = InlineKeyboardBuilder()
    kb.button(text='Редактировать объявление', callback_data=f'update_advertisement:{adv_id}')
    return kb.as_markup()


def advertisement_fields_for_update_kb(adv_id: int):
    kb = InlineKeyboardBuilder()
    fields = [
        ('title', 'Название'),
        ('operation_type', 'Тип операции'),
        ('description', 'Описание'),
        ('district', 'Район'),
        ('address', 'Адрес'),
        ('property_category', 'Категория недвижимости'),
        ('property_type', 'Тип недвижимости'),
        ('price', 'Цена'),
        ('quadrature_from', 'Квадратура от'),
        ('quadrature_to', 'Квадратура до'),
        ('creation_date', 'Дата постройки'),
        ('rooms_from', 'Кол-во комнат от'),
        ('rooms_to', 'Кол-во комнат до'),
        ('floor_from', 'Этаж от'),
        ('floor_to', 'Этаж до'),
        ('repair_type', 'Тип ремонта'),
        ('house_quadrature', 'Площадь дома'),
        ('is_studio', 'Студия'),
    ]

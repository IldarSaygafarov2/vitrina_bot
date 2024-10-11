from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton, ReplyKeyboardMarkup
from services.api import api_manager


def start_kb():
    reply_builder = ReplyKeyboardBuilder()
    reply_builder.add(
        KeyboardButton(text='Создать объявление'),
        KeyboardButton(text='Мои объявления')
    )
    reply_builder.adjust(2, 2)
    return reply_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def main_categories_kb():
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [KeyboardButton(text='Аренда'), KeyboardButton(text='Покупка')]
        ]
    )
    return markup




def property_type_kb():
    reply_builder = ReplyKeyboardBuilder()
    reply_builder.add(
        KeyboardButton(text='Новостройка'),
        KeyboardButton(text='Вторичный фонд')
    )
    return reply_builder.as_markup()


"""
        WITH = 'with', 'С ремонтом'
        WITHOUT = 'without', 'Без ремонта'
        DESIGNED = 'designed', 'Дизайнерский ремонт'
        ROUGH = 'rough', 'Черновая'
        PRE_FINISHED = 'pre_finished', 'Предчистовая'
"""


def repair_type_kb():
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text='С ремонтом'),
                KeyboardButton(text='Без ремонта')
            ],
            [
                KeyboardButton(text='Дизайнерский ремонт'),
                KeyboardButton(text='Черновая'),
            ],
            [KeyboardButton(text='Предчистовая')]
        ]
    )
    return markup


def property_categories_kb():
    categories = api_manager.category_service.get_categories()
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [KeyboardButton(text=category['name']) for category in categories]
        ]
    )
    return kb


def is_auction_allowed_kb():
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [KeyboardButton(text='Да'), KeyboardButton(text='Нет')]
        ]
    )
    return kb


def is_studio_kb():
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text='Да'),
                KeyboardButton(text='Нет')
            ]
        ]
    )
    return kb


def rg_start_kb():
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text='Список риелторов'),
                KeyboardButton(text='Последние объявления')
            ]
        ]
    )
    return kb


def ad_moderated_kb():
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text='Проверенные'),
                KeyboardButton(text='Непроверенные')
            ]
        ]
    )
    return kb
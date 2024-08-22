from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton, ReplyKeyboardMarkup
from api import ApiService


def start_kb():
    reply_builder = ReplyKeyboardBuilder()
    reply_builder.add(
        KeyboardButton(text='Создать объявление')
    )
    return reply_builder.as_markup()


def main_categories_kb():
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [KeyboardButton(text='Аренда'), KeyboardButton(text='Покупка')]
        ]
    )
    return markup


def districts_kb():
    districts = ApiService().get_districts()
    reply_builder = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [KeyboardButton(text=district['name'])] for district in districts
        ])
    return reply_builder


def property_type_kb():
    reply_builder = ReplyKeyboardBuilder()
    reply_builder.add(
        KeyboardButton(text='Новостройка'),
        KeyboardButton(text='Вторичный фонд')
    )
    return reply_builder.as_markup()


def repair_type_kb():
    markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [
                KeyboardButton(text='С ремонтом'),
                KeyboardButton(text='Коробка без ремонта')
             ]
        ]
    )
    return markup


def property_categories_kb():
    categories = ApiService().get_categories()
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        one_time_keyboard=True,
        keyboard=[
            [KeyboardButton(text=category['name']) for category in categories]
        ]
    )
    return kb
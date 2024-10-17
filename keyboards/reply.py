from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton, ReplyKeyboardMarkup
from services.api import api_manager


def start_kb():
    reply_builder = ReplyKeyboardBuilder()
    reply_builder.add(
        KeyboardButton(text='Создать объявление'),
        KeyboardButton(text='Мои объявления')
    )
    reply_builder.adjust(2)
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
    return reply_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


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

from telebot import types


def create_ad_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(
        types.KeyboardButton(text='Создать объявление')
    )
    return markup

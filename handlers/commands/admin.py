from telebot import types

from data.loader import bot
from keyboards import reply


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    chat_id = message.chat.id
    username = message.from_user.username
    bot.send_message(chat_id, f'Привет, {username}', reply_markup=reply.create_ad_markup())

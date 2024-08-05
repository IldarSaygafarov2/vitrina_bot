from data.loader import bot
from telebot import types


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    chat_id = message.chat.id
    username = message.from_user.username
    bot.send_message(chat_id, f'Привет, {username}')



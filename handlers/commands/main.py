from telebot import types
from data.loader import bot


@bot.message_handler(commands=['start'])
def start(message: types.Message) -> None:
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Hello user')

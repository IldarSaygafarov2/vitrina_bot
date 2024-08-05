from telebot import TeleBot

import settings

bot = TeleBot(token=settings.BOT_TOKEN, use_class_middlewares=True)

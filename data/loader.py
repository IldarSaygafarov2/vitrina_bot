from telebot import TeleBot
from telebot import custom_filters
from telebot.storage import StateMemoryStorage

import settings

state_storage = StateMemoryStorage()
bot = TeleBot(token=settings.BOT_TOKEN, state_storage=state_storage)


# bot.add_custom_filter(custom_filters.StateFilter(bot))

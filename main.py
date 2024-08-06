from telebot import custom_filters

import handlers
from data.loader import bot


def main() -> None:
    print('bot started')
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.infinity_polling(skip_pending=True)


if __name__ == '__main__':
    main()


import handlers
from data.loader import bot


def main() -> None:
    print('bot started')
    bot.infinity_polling()


if __name__ == '__main__':
    main()


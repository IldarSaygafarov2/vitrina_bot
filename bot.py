import asyncio
import logging
import sys
from datetime import datetime

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

import settings
from handlers import routers_list


async def main():

    bot = Bot(token=settings.BOT_TOKEN,
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_routers(*routers_list)
    await dp.start_polling(bot)


if __name__ == '__main__':
    formatter = '[%(asctime)s] %(levelname)8s --- %(message)s (%(filename)s:%(lineno)s)'
    logging.basicConfig(
        filename=f'logs/bot-from-{datetime.now().date()}.log',
        filemode='w',
        format=formatter,
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.WARNING,
        encoding='utf-8'
    )
    # logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    print('bot started')
    asyncio.run(main())

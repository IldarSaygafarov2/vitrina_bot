import asyncio
import logging
import sys

from data.loader import bot, dp
from handlers import routers_list


async def main():
    dp.include_routers(*routers_list)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

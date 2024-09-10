import asyncio
import logging
import sys

from data.loader import bot, dp
from handlers import advertisement, simple_user, rg


async def main():
    dp.include_routers(advertisement.router)
    dp.include_routers(rg.router)
    dp.include_routers(simple_user.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

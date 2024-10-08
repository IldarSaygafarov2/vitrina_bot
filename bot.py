import asyncio
import logging
import sys

from data.loader import bot, dp
from handlers import advertisement, simple_user, rg


async def main():
    dp.include_router(rg.router)
    dp.include_router(advertisement.router)
    dp.include_router(simple_user.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

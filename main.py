import asyncio
import logging
import sys

from data.loader import bot, dp
from handlers import advertisement, simple_user, rg
import requests

# url = 'http://127.0.0.1:8000/api/v1/'
# print(requests.get('http://127.0.0.1:8000/api/v1/districts/', headers={'Accept-Language': 'uz'}).json())


async def main():
    dp.include_routers(advertisement.router)
    dp.include_routers(rg.router)
    dp.include_routers(simple_user.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

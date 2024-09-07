# imports ________________________________________________________

# asyncio
import asyncio
# logging
import logging
# sys
from sys import stdout

# aiohttp
import aiohttp
# aiogram
from aiogram import Bot, Dispatcher
# aiogram defaults
from aiogram.client.default import DefaultBotProperties
# aiogram enums
from aiogram.enums import ParseMode

# tokens
from config import TOKEN

# bot settings ___________________________________________________

# bot
default: DefaultBotProperties = DefaultBotProperties(parse_mode=ParseMode.HTML)
bot: Bot = Bot(token=TOKEN, default=default)


# bot running ____________________________________________________


# main
async def main() -> None:
    # dispatcher
    from handlers import setup_routers

    dp: Dispatcher = Dispatcher()
    dp.include_router(router=setup_routers())

    await dp.start_polling(bot)


# run
if __name__ == "__main__":
    # logging
    logging.basicConfig(level=logging.DEBUG, stream=stdout)

    # asyncio run
    asyncio.run(main())

# aiohttp session
session: aiohttp.ClientSession = aiohttp.ClientSession(trust_env=True)

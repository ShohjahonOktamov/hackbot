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

# httpserver
from http.server import HTTPServer, SimpleHTTPRequestHandler

# threading
import threading

# bot settings ___________________________________________________

# bot
default: DefaultBotProperties = DefaultBotProperties(parse_mode=ParseMode.HTML)
bot: Bot = Bot(token=TOKEN, default=default)


# bot running ____________________________________________________


def run_http_server():
    httpd = HTTPServer(("", 80), SimpleHTTPRequestHandler)
    print("Starting HTTP server on port 80...")
    httpd.serve_forever()


# main
async def main() -> None:
    # dispatcher
    from handlers import setup_routers

    dp: Dispatcher = Dispatcher()
    dp.include_router(router=setup_routers())

    await dp.start_polling(bot)


# run
if __name__ == "__main__":
    # serving httpserver
    http_thread = threading.Thread(target=run_http_server, daemon=True)
    http_thread.start()
    
    # logging
    logging.basicConfig(level=logging.DEBUG, stream=stdout)

    # asyncio run
    asyncio.run(main())

# aiohttp session
session: aiohttp.ClientSession = aiohttp.ClientSession(trust_env=True)

import json
from typing import Any

from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, ReplyKeyboardRemove
from aiohttp.formdata import FormData
from fake_useragent import UserAgent

from bot import session
from config import TOKEN




def clean_keyboard_dict(data: dict | list) -> dict | list:
    if isinstance(data, dict):
        items: tuple[Any, ...] = tuple(data.items())
        for key, value in items:
            if value is None:
                del data[key]
            elif isinstance(value, dict):
                clean_keyboard_dict(value)
            elif isinstance(value, list):
                for item in value:
                    clean_keyboard_dict(item)
    elif isinstance(data, list):
        for item in data:
            clean_keyboard_dict(item)
    return data


async def send_message_hashable(chat_id: int, text: str,
                                reply_markup: ReplyKeyboardMarkup | InlineKeyboardMarkup | ReplyKeyboardRemove | None = None) -> None:
    url: str = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    form: FormData = FormData()

    form.add_field(name="chat_id", value=str(chat_id))
    form.add_field(name="text", value=text)
    form.add_field(name="parse_mode", value="HTML")

    if reply_markup is not None:
        form.add_field(name="reply_markup", value=json.dumps(clean_keyboard_dict(reply_markup.dict())))
    # async with session.post(url=url, data=form) as response:
    #     print(await response.json())
    await session.post(url=url, data=form)


async def send_message_to_number(number: str) -> None:
    url: str = "https://api.marsit.uz/api/v2/auth/send_code"

    ua: UserAgent = UserAgent()

    headers: dict[str, str] = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Language": "uz,ru-RU;q=0.9,ru;q=0.8,en-US;q=0.7,en;q=0.6",
        "Connection": "keep-alive",
        "Content-Type": "application/json",
        "Origin": "https://space.marsit.uz",
        "Referer": "https://space.marsit.uz/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": ua.random,
        "sec-ch-ua": '"Not A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        "sec-ch-ua-mobile": "?1",
        "sec-ch-ua-platform": '"Android"'
    }

    data: dict[str, str] = {
        "phone": number
    }

    # async with session.post(url=url, json=data, headers=headers) as response:
    #     print(await response.json())
    await session.post(url=url, json=data, headers=headers)

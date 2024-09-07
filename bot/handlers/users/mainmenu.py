# imports ________________________________________________________
# asyncio
import asyncio
# regex
import re
# socket
import socket
# typing
from typing import Any, Coroutine

# ipinfo
import ipinfo
# --- aiogram ---
# Router
from aiogram import Router, F
# FSM
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.methods.send_message import SendMessage
# types
from aiogram.types import Message, ReplyKeyboardMarkup, InlineKeyboardMarkup, ReplyKeyboardRemove
# buttons
from buttons.users import back_kb, main_menu_kb
# ip info access token, root url
from config import ipinfo_access_token, url
# functions
from functions import send_message_hashable, send_message_to_number
# states
from states.users import MainMenuStates

# api calls
# from bot.api import get_tguser, post_tguser, patch_tguser

# settings ________________________________________________
# router
router: Router = Router()

# ipinfo
ip_handler: ipinfo.AsyncHandler = ipinfo.getHandlerAsync(access_token=ipinfo_access_token)

# ip ranges not to scan
private_ip_ranges: list[str] = [
    "10.",
    "172.16.",
    "192.168.",
    "127.0.0.1",
    "localhost",
    "169.254.",
    "::1",
    "fe80:"
]


# indicators: tuple[str, str, str, str, str, str, str, str, str] = ("/", "-", "\\", "|", "/", "-", "\\", "|", "/")


async def scanning(message: Message) -> None:
    await message.edit_text(text="🔎 Scanning.")
    await message.edit_text(text="🔎 Scanning..")
    await message.edit_text(text="🔎 Scanning...")
    await message.edit_text(text="🔎 Scanning....")
    await message.edit_text(text="🔎 Scanning....")


async def sending(message: Message) -> None:
    await message.edit_text(text="💣 Sending Bomber.")
    await message.edit_text(text="💣 Sending Bomber..")
    await message.edit_text(text="💣 Sending Bomber...")
    await message.edit_text(text="💣 Sending Bomber....")
    await message.edit_text(text="💣 Sending Bomber.....")


async def interrupt(message: Message, answer: str, state: FSMContext | None = None, state1: FSMContext | None = None,
                    keyboard: ReplyKeyboardMarkup | InlineKeyboardMarkup | ReplyKeyboardRemove | None = None) -> None:
    tasks: list[Coroutine[Any, Any, None] | SendMessage] = []
    if state is not None:
        tasks.append(state.set_state(state1))

    tasks.append(send_message_hashable(chat_id=message.from_user.id, text=answer, reply_markup=keyboard))

    await asyncio.gather(*tasks)


async def get_ip_info(ip_address: str) -> dict[str, str | bool | dict[str, str]]:
    try:
        details: dict[str, str | bool] = (
            await ip_handler.getDetails(ip_address=ip_address)
        ).details
        if "bogon" not in details.keys():
            details["success"] = True
        else:
            details["success"] = False
    except ValueError:
        details: dict[str, bool] = {"success": False}
    return details


async def scan_port(host: str, port: int) -> int | None:
    try:
        reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout=5)
        writer.close()
        await writer.wait_closed()
        return port
    except (ConnectionRefusedError, asyncio.TimeoutError):
        return None


async def scan_ports(host: str, ports: range) -> list[int]:
    tasks = [scan_port(host=host, port=port) for port in ports]

    results: tuple[int | None] = await asyncio.gather(*tasks)

    open_ports: list[int] = [result for result in results if result is not None]

    return open_ports


# handlers _______________________________________________________


@router.message(F.text == "📷 Cam & 🌎 Geo Hack", MainMenuStates.main_menu)
async def camhack(message: Message) -> None:
    answer: str = (
        f"<b>Your link is: </b>{url}h/{message.from_user.id}\n<b>Send it to your victim to get frontal camera photo "
        f"and geolocation\n\n©️ EnigmaH.pythonanywhere.com</b>"
    )

    await message.answer(text=answer)


@router.message(F.text == "🔎 IP Info", MainMenuStates.main_menu)
async def ip_info(message: Message, state: FSMContext) -> None:
    answer: str = "<b>Enter a valid IP-Address to get detailed information about it</b>"
    state1: State = MainMenuStates.ipinfo
    keyboard: ReplyKeyboardMarkup = back_kb

    await asyncio.gather(send_message_hashable(chat_id=message.from_user.id, text=answer, reply_markup=keyboard),
                         state.set_state(state=state1))


@router.message(F.text == "🔙 Back", MainMenuStates.ipinfo)
async def back_to_main_menu_from_ip_info(message: Message, state: FSMContext) -> None:
    answer: str = "<b>Main menu</b>"
    keyboard: ReplyKeyboardMarkup = main_menu_kb
    state1: State = MainMenuStates.main_menu

    await asyncio.gather(send_message_hashable(chat_id=message.from_user.id, text=answer, reply_markup=keyboard),
                         state.set_state(state=state1))


@router.message(F.text, MainMenuStates.ipinfo)
async def send_ip_info(message: Message):
    details: dict[str, str | bool | dict[str, str]] = await get_ip_info(
        ip_address=message.text
    )
    if details["success"]:
        answer: str = f"""
<b>🌐 IP-Address: {details["ip"]}</b>
<b>🏢 Organization:</b> {details.get("org", '?')}
<b>📡 Hostname:</b> {details.get("hostname", '?')}

<b>🌍 Continent:</b> {details.get("continent", {}).get("name")}
<b>🏳️ Country:</b> {details.get("country_flag", {}).get("emoji", '?')} {details.get("country_name", '?')} ({details.get("country", '?')})
<b>🌆 Region:</b> {details.get("region", '?')}
<b>🏙 City:</b> {details.get("city", '?')}
<b>🕔 Timezone:</b> {details.get("timezone", '?')}

<b>Latitude:</b> {details["latitude"]}
<b>Longitude:</b> {details["longitude"]}

<a href="https://EnigmaH.pythonanywhere.com"><b>©️ EnigmaH.pythonanywhere.com</b></a>"""

        await message.answer_location(
            latitude=details["latitude"], longitude=details["longitude"]
        )
    else:
        answer: str = "<b>Invalid IP-Address, please, send a valid IP-Address</b>"
    await message.answer(text=answer)


@router.message(F.text == "📡 Port Scanner", MainMenuStates.main_menu)
async def port_scanner(message: Message, state: FSMContext) -> None:
    answer: str = """<b>
Enter the host and the port(s) to scan.
Format examples:
1. To scan a range of ports: example.com 1-10000
2. To scan a single port: example.com 443
</b>"""
    keyboard = back_kb
    state1: State = MainMenuStates.port_scan

    await asyncio.gather(send_message_hashable(chat_id=message.from_user.id, text=answer, reply_markup=keyboard),
                         state.set_state(state=state1))


@router.message(F.text == "🔙 Back", MainMenuStates.port_scan)
async def back_to_main_menu_from_port_scan(message: Message, state: FSMContext) -> None:
    answer: str = "<b>Main menu</b>"
    keyboard: ReplyKeyboardMarkup = main_menu_kb
    state1: State = MainMenuStates.main_menu

    await asyncio.gather(send_message_hashable(chat_id=message.from_user.id, text=answer, reply_markup=keyboard),
                         state.set_state(state=state1))


@router.message(F.text, MainMenuStates.port_scan)
async def send_scanned_ports(message: Message) -> None:
    scan_data: list[str] = message.text.split()
    if len(scan_data) != 2:
        await interrupt(message=message, answer="Please, specify both the host and port")

        return

    host: str = scan_data[0]

    for prefix in private_ip_ranges:
        if host.startswith(prefix):
            await interrupt(message=message, answer="Invalid host. Please enter a valid host.")

            return

    ports: list = scan_data[1].split('-')

    try:
        socket.gethostbyname(host)
    except socket.gaierror:
        await interrupt(message=message, answer="Invalid host. Please enter a valid host.")

        return

    if len(ports) == 2:
        try:
            start, end = map(int, ports)

            if start < 1 or end > 65535 or start > end:
                await interrupt(message=message, answer="Invalid ports range. Please, enter a valid ports range")

                return

            if end - start > 9999:
                await interrupt(message=message, answer="Sorry, the maximum number of port ranges per scan is 10 000.")

                return

        except ValueError:
            await interrupt(message=message, answer="Invalid ports range. Please, enter a valid ports range")

            return

        progress: Message = await message.answer("🔎 Scanning")

        task: asyncio.Task = asyncio.create_task(scanning(message=progress))

        open_ports: list[int] = await scan_ports(host=host, ports=range(start, end + 1))

        task.cancel()

        await progress.edit_text(text="✅ Done")

        if not open_ports:
            await message.answer("No open ports were found")

            return

        answer = "Open ports:\n"

        answer += '\n'.join(map(str, open_ports))

        await message.answer(text=answer)

    elif len(ports) == 1:
        try:
            port = int(ports[0])
            if not 0 < port < 65536:
                await interrupt(message=message, answer="Invalid port. Please, enter a valid port")

                return
        except ValueError:
            await interrupt(message=message, answer="Invalid port. Please, enter a valid port")

            return
        port_open: int | None = await scan_port(host=host, port=port)
        if port_open is None:
            await message.answer(f"The port {port} is not open")

            return

        await message.answer(text=f"The port {port} is open")


@router.message(F.text == "💣 SMS Bomber", MainMenuStates.main_menu)
async def sms_bomber(message: Message, state: FSMContext) -> None:
    answer: str = """<b>
    Enter the phone number to bomb and the number of messages
Format example:
+999881234567
20

Supported country codes:
+998 (UZ)
    </b>"""
    keyboard = back_kb
    state1: State = MainMenuStates.sms_bomber

    await asyncio.gather(send_message_hashable(chat_id=message.from_user.id, text=answer, reply_markup=keyboard),
                         state.set_state(state=state1))


@router.message(F.text == "🔙 Back", MainMenuStates.sms_bomber)
async def back_to_main_menu_from_sms_bomber(message: Message, state: FSMContext) -> None:
    answer: str = "<b>Main menu</b>"
    keyboard: ReplyKeyboardMarkup = main_menu_kb
    state1: State = MainMenuStates.main_menu

    await asyncio.gather(send_message_hashable(chat_id=message.from_user.id, text=answer, reply_markup=keyboard),
                         state.set_state(state=state1))


@router.message(F.text, MainMenuStates.sms_bomber)
async def bomb_number(message: Message, state: FSMContext) -> None:
    input_data: list[str] = message.text.split('\n')
    if len(input_data) != 2:
        answer: str = "<b>Wrong input format!</b>"
        await interrupt(message=message, answer=answer)
        return

    number: str = input_data[0]

    pattern: str = r"^\+998(20|33|50|55|61|62|65|66|67|69|70|71|72|73|74|75|76|77|88|90|91|92|93|94|95|96|97|98|99)\d{7}$"

    if not re.match(pattern=pattern, string=number):
        answer: str = "<b>Invalid phone number!</b>"
        await interrupt(message=message, answer=answer)
        return

    try:
        sms_count: int = int(input_data[1])
        if sms_count < 1:
            answer: str = "<b>You can't send 0 or below messages!</b>"
            await interrupt(message=message, answer=answer)
            return
        elif sms_count > 50:
            answer: str = "<b>You can't send more than 50 messages!</b>"
            await interrupt(message=message, answer=answer)
            return
    except ValueError:
        answer: str = "<b>Messages count must be a valid integer!</b>"
        await interrupt(message=message, answer=answer)
        return

    progress: Message = await message.answer("💣 Sending Bomber.")

    task: asyncio.Task = asyncio.create_task(sending(message=progress))

    tasks: list = [send_message_to_number(number=number) for _ in range(sms_count)]

    await asyncio.gather(*tasks)

    task.cancel()

    await progress.edit_text(text="✅ Done")

# ________________________________________________________________

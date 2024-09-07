# imports ________________________________________________________
# typing
import asyncio
from typing import Any

# aiogram
# Router
from aiogram import Router, F
# filters
from aiogram.filters import CommandStart
# states
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
# types
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    Contact,
    ReplyKeyboardRemove,
    CallbackQuery,
)
from api import get_tguser, post_tguser, patch_tguser
# buttons
from buttons.users import share_number_kb, agreement_kb, main_menu_kb
# functions
from functions import send_message_hashable
from states.users import StartStates, MainMenuStates

# bot

# settings ________________________________________________
# router
router: Router = Router()


# handlers _______________________________________________________


@router.message(CommandStart())
async def start(message: Message, state: FSMContext) -> None:
    tguser: dict[str, Any] = await get_tguser(pk=message.from_user.id)
    if tguser["exists"]:
        if tguser["tguser"]["phone_number"] is not None:
            if tguser["tguser"]["agreement"]:
                answer: str = "<b>Main menu</b>"
                keyboard: ReplyKeyboardMarkup = main_menu_kb
                state1: State = MainMenuStates.main_menu
            else:
                answer: str = """<b>
!!! Warning !!!

This bot is for ethical & educational purposes only.

We are not responsible if you harm others or do illegal activities through using this bot, use this bot at your own 
risk.

By using this bot you agree to be bound by our terms.

©️ EnigmaH.pythonanywhere.com
</b>
"""
                keyboard: InlineKeyboardMarkup = agreement_kb
                state1 = StartStates.agreement
        else:
            answer: str = (
                "<b>Before you start using this bot, please, share your phone number by clicking the button below</b>"
            )
            keyboard: ReplyKeyboardMarkup = share_number_kb
            state1: State = StartStates.share_phone_number_state

    else:
        pk: int = message.from_user.id
        first_name: str = message.from_user.first_name
        last_name: str | None = message.from_user.last_name
        username: str | None = message.from_user.username
        data: dict[str, Any] = {
            "user_id": pk,
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
        }
        await post_tguser(data=data)
        answer: str = (
            "<b>Before you start using this bot, please, share your phone number by clicking the button below</b>"
        )
        keyboard: ReplyKeyboardMarkup = share_number_kb
        state1: State = StartStates.share_phone_number_state

    await asyncio.gather(send_message_hashable(chat_id=message.from_user.id, text=answer, reply_markup=keyboard),
                         state.set_state(state1))


@router.message(F.contact, StartStates.share_phone_number_state)
async def phone_number_handled(message: Message, state: FSMContext) -> None:
    contact: Contact = message.contact
    pk: int = message.from_user.id
    if contact.user_id == pk:
        pk: int = message.from_user.id
        first_name: str = message.from_user.first_name
        last_name: str | None = message.from_user.last_name
        username: str | None = message.from_user.username
        data: dict[str, Any] = {
            "user_id": pk,
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "phone_number": int(contact.phone_number),
        }
        await patch_tguser(pk, data=data)
        answer: str = """<b>
!!! Warning !!!

This bot is for ethical & educational purposes only.

We are not responsible if you harm others or do illegal activities through using this bot, use this bot at your own 
risk.

By using this bot you agree to be bound by our terms.

©️ EnigmaH.pythonanywhere.com
</b>
"""
        keyboard: InlineKeyboardMarkup = agreement_kb
        state1: State = StartStates.agreement
        await message.reply(
            text="<b>Accepted ✅</b>",
            reply_markup=ReplyKeyboardRemove(),
        )

    else:
        answer: str = (
            "<b>Please, send your own phone number by clicking the button below</b>"
        )
        keyboard: ReplyKeyboardMarkup = share_number_kb
        state1: State = StartStates.share_phone_number_state

    await asyncio.gather(send_message_hashable(chat_id=message.from_user.id, text=answer, reply_markup=keyboard),
                         state.set_state(state1))


@router.callback_query(F.data == "agree", StartStates.agreement)
async def agreed(callback_query: CallbackQuery, state: FSMContext) -> None:
    pk: int = callback_query.from_user.id

    answer: str = "<b>Main menu</b>"
    keyboard: ReplyKeyboardMarkup = main_menu_kb
    state1: State = MainMenuStates.main_menu

    await asyncio.gather(patch_tguser(pk=pk, data={"agreement": True}),
                         send_message_hashable(
                             chat_id=pk,
                             text=answer,
                             reply_markup=keyboard,
                         ),
                         state.set_state(state1))

# ________________________________________________________________

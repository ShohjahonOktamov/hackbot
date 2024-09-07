from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

share_number_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Share my phone number 📱", request_contact=True)]],
    resize_keyboard=True,
)

agreement_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="I Agree", callback_data="agree")]]
)

main_menu_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📷 Cam & 🌎 Geo Hack")],
        [KeyboardButton(text="🔎 IP Info"), KeyboardButton(text="📡 Port Scanner"), KeyboardButton(text="🌐 Web Screen")],
        [KeyboardButton(text="💣 SMS Bomber")]
    ],
    resize_keyboard=True,
)

back_kb: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔙 Back")],
    ],
    resize_keyboard=True,
)

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

wallet_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='❔ Как использовать кошелек', callback_data='use_wallet')
        ],
        [
            InlineKeyboardButton(text='💲 Реферальная система', callback_data='ref')
        ]
    ]
)

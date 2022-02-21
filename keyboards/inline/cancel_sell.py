from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

keyboard_cancel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='⏪ Отмена', callback_data='cancel_sell')
        ]
    ]
)
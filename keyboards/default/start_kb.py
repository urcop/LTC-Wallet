from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton('➕ Купить LTC'),
            KeyboardButton('➖ Продать LTC')
        ],
        [
            KeyboardButton('💲 Кошелек')
        ],
        [
            KeyboardButton('🔝 Стать бета-тестером')
        ]
    ], resize_keyboard=True
)

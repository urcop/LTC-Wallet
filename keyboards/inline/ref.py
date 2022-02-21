from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def ref_keyboard(tg_id):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='🔝 Пригласить',
                                     url=f'https://t.me/share/url?url=https://t.me/LiteWalletRobot/?start={tg_id}')
            ]
        ]
    )
    return keyboard

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

answer_callback = CallbackData('user', 'id', 'state')


def gen_answer_keyboard(tg_id):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='🟢 Ответить',
                                     callback_data=answer_callback.new(id=tg_id, state='answer_msg'))
            ]
        ]
    )
    return keyboard


sup_cancel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='🔴 Отмена', callback_data='cancel_answer')
        ]
    ]
)

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

user_callback = CallbackData('user', 'id', 'state')


def generate_keyboard(id):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Заблокировать вывод', callback_data=user_callback.new(id=id, state='close'))
            ],
            [
                InlineKeyboardButton(text='Разблокировать вывод', callback_data=user_callback.new(id=id, state='open'))
            ],
            [
                InlineKeyboardButton(text='Пополнить баланс', callback_data=user_callback.new(id=id, state='give_bal'))
            ],
            [
                InlineKeyboardButton(text='Забрать баланс', callback_data=user_callback.new(id=id, state='take_bal'))
            ]
        ]
    )
    return keyboard

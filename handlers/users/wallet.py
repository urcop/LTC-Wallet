from aiogram import types
from aiogram.types import CallbackQuery

from keyboards.inline import wallet_keyboard, ref_keyboard
from loader import dp, db


@dp.message_handler(text='💲 Кошелек')
async def wallet(message: types.Message):
    user = await db.select_user(tg_id=int(message.from_user.id))
    text = f'💲 ID: {user["tg_id"]} \n\n' \
           f'💲 Баланс: {user["balance"]} LTC - {user["balance"] * 8495.39}₽'
    await message.answer(text=text, reply_markup=wallet_keyboard)


@dp.callback_query_handler(text='ref')
async def get_ref_url(call: CallbackQuery):
    await call.message.delete()
    text = f'Ваша реферальная ссылка: https://t.me/LiteWalletRobot?start={call.from_user.id}'
    await call.message.answer(text=text, reply_markup=ref_keyboard(call.from_user.id))

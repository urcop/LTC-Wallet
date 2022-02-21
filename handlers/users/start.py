import asyncpg.exceptions
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default import keyboard
from loader import dp, db


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    try:
        if len(message.text.split(' ')) == 2:
            ref = message.text.split(' ')[1]
            await db.add_user(
                tg_id=message.from_user.id,
                fullname=message.from_user.full_name,
                username=message.from_user.username,
                referral=int(ref)
            )
        else:
            await db.add_user(
                tg_id=message.from_user.id,
                fullname=message.from_user.full_name,
                username=message.from_user.username,
                referral=0
            )
        await message.answer(f"👋 <b>Привет, {message.from_user.full_name}!</b>\n\n"
                             f"<i>Это телеграм бот от компании LiteWallet для обмена криптовалюты Litecoin (LTC) и фиатных"
                             f"денег. А также быстрый и бесплатный кошелек!</i>", reply_markup=keyboard)
    except asyncpg.exceptions.UniqueViolationError:
        await message.answer('👋 <b>Добро пожаловать! Мы рады видеть вас снова.</b>', reply_markup=keyboard)

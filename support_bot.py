import logging

import typing
from aiogram import executor
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import CallbackQuery

from data.config import ADMINS
from keyboards.default import support_keyboard
from keyboards.inline import sup_cancel
from keyboards.inline.support import gen_answer_keyboard, answer_callback
from loader import dp, db
import middlewares, handlers
from states.user_state import SupportMsg, Answer

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from data import config
from loader import db
from utils.set_bot_commands import set_default_commands

current_user = 0


async def on_startup(dispatcher):
    # Устанавливаем дефолтные команды
    await set_default_commands(dispatcher)
    logging.info('Подключение к бд')
    await db.create()
    logging.info('Создание таблицы пользователей')
    await db.create_table_users()


bot = Bot(token=config.SUPPORT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(CommandStart())
async def start_support(message: types.Message):
    await message.answer("👋 Здравствуйте, чем могу Вам помочь?")


@dp.message_handler()
async def question(message: types.Message):
    try:
        ref = await db.select_user(tg_id=int(message.from_user.id))
        if ref['referral'] == 0:
            text = f'[ Пользователь - @{message.from_user.username} ({message.from_user.full_name}) ' \
                   f'id - {message.from_user.id}]\n' \
                   f'Реферал - 0\n\n'
        else:
            referral = await db.select_user(tg_id=int(ref['referral']))
            text = f'[ Пользователь - @{message.from_user.username} ({message.from_user.full_name}) ' \
                   f'id - {message.from_user.id}]\n' \
                   f'Реферал - id {referral["tg_id"]} - @{referral["username"]}\n\n'
        data = text + message.text
        for admin in ADMINS:
            await bot.send_message(chat_id=admin, text=data,
                                   reply_markup=gen_answer_keyboard(str(ref["tg_id"])))
    except Exception as e:
        logging.info(e)


@dp.callback_query_handler(answer_callback.filter())
async def answer_message(call: CallbackQuery):
    data = call.data.split(':')
    global current_user
    current_user = data[1]
    await call.message.delete()
    await call.message.answer('Введите сообщение для пользователя', reply_markup=sup_cancel)
    await Answer.message.set()


@dp.message_handler(state=Answer.message)
async def get_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['message'] = message.text
        await bot.send_message(chat_id=current_user, text=data['message'])
        await state.finish()


@dp.callback_query_handler(text='cancel_answer', state=Answer.message)
async def cancel_message(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer('Отменено!')
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)

import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils import callback_data

from data.config import ADMINS
from keyboards.inline import generate_keyboard, keyboard_cancel
from keyboards.inline.admin_kb import user_callback
from loader import dp, db
from states.user_state import SelectPerson, BalanceTake, BalanceGive

current_user = 0


@dp.message_handler(text=['.search', '/search', '!search'])
async def search_user(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        await message.answer('Введите id или username пользователя с @')
        await SelectPerson.id_or_nik.set()
    else:
        pass


@dp.message_handler(state=SelectPerson.id_or_nik)
async def user_params(message: types.Message, state: FSMContext):
    global current_user
    async with state.proxy() as data:
        try:
            data['id_or_nik'] = message.text
            if data['id_or_nik'][0] == '@':
                user = await db.select_user(username=data['id_or_nik'][1:])
            else:
                user = await db.select_user(tg_id=int(data['id_or_nik']))
            await message.answer(f'Вы выбрали - @{user["username"]} ({user["fullname"]})',
                                 reply_markup=generate_keyboard(str(data['id_or_nik'])))
            current_user = int(user["tg_id"])

            await state.finish()
        except Exception as e:
            logging.info(e)
            await message.answer('Пользователь не найден пропишите еще раз команду поиска')
            await state.finish()


@dp.callback_query_handler(user_callback.filter())
async def state_to_user(call: CallbackQuery):
    data = call.data.split(':')
    if data[1][0] == '@':
        user = await db.select_user(username=data[1][1:])
    else:
        user = await db.select_user(tg_id=int(data[1]))
    usr_id = user["tg_id"]
    if data[2] == 'close':
        await db.update_is_sell(False, int(usr_id))
        await call.message.answer('Успешно!')
    elif data[2] == 'open':
        await db.update_is_sell(True, int(usr_id))
        await call.message.answer('Успешно!')
    elif data[2] == 'give_bal':
        await call.message.answer(f'Сколько начислить баланса? Текущий баланс - {user["balance"]}')
        await BalanceGive.count.set()
    else:
        await call.message.answer(f'Сколько забрать баланса? Текущий баланс - {user["balance"]}')
        await BalanceTake.count.set()

    await call.message.delete()


@dp.message_handler(state=BalanceGive.count)
async def give_bal(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["id"] = current_user
        data["count"] = message.text
        await db.add_balance(tg_id=data["id"], balance=float(data["count"]))
        await state.finish()
        await message.answer('Начислено!')


@dp.message_handler(state=BalanceTake.count)
async def give_bal(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["id"] = current_user
        data["count"] = message.text
        await db.take_balance(tg_id=data["id"], balance=float(data["count"]))
        await state.finish()
        await message.answer('Забрано!')

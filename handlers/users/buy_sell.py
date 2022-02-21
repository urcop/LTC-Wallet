from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline import keyboard_cancel
from loader import dp, db
from states.user_state import SellLtc


@dp.message_handler(text='➕ Купить LTC')
async def buy_ltc(message: types.Message):
    await message.answer('💸 В связи с перегрузкой сервера, пополнения переведены в ручной режим. \n '
                         '❔ Хотите пополнить? - Напишите в <a href="https://t.me/LiteWalletSupportRobot">техническую '
                         'поддержку</a>.')


@dp.message_handler(text='➖ Продать LTC')
async def buy_ltc(message: types.Message):
    balance = await db.get_balance(tg_id=int(message.from_user.id))
    await message.answer('❌ Вывод недоступен\n\n'
                         f'Обратитесь в <a href="https://t.me/LiteWalletSupportRobot">техническую поддержу</a></i>')
    # await SellLtc.count.set()


@dp.message_handler(state=SellLtc.count)
async def count_ltc(message: types.Message, state: FSMContext):
    user = await db.select_user(tg_id=int(message.from_user.id))
    async with state.proxy() as data:
        data['count'] = message.text
        if data['count'][0] == '0':
            await message.answer('🔴 Некорректное значение\n '
                                 'Введите сумму > 0 или нажмите кнопку Отмена')
        else:
            try:
                balance = await db.get_balance(tg_id=int(message.from_user.id))
                if float(data['count']) > balance['balance']:
                    await message.answer('🔴 Недостаточно средств')
                else:
                    if user["is_sell"]:
                        await message.answer(
                            '🔴 Ошибка вывода\n '
                            'Обратитесь в <a href="https://t.me/LiteWalletSupportRobot">техническую поддержу</a>')
                        await state.finish()
                    else:
                        await message.answer('🔴 В данный момент вывод средств запрещен')
                        await state.finish()
            except Exception:
                await message.answer('🔴 Некорректное значение\n'
                                     'Введите другое значение или нажмите кнопку Отмена!')


@dp.callback_query_handler(text='cancel_sell', state=SellLtc.count)
async def cancel_sell(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Отменено!')
    await call.message.delete()
    await state.finish()

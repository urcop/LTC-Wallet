from aiogram import types

from loader import dp


@dp.message_handler(text='🔝 Стать бета-тестером')
async def start_beta(message: types.Message):
    text = '<i>🔝 Команда LiteWallet ищет заинтересованных лиц для улучшения проекта. \n\n' \
           'На данный момент требуются бета-тестеры, чтобы обнаружить и исправить все моменты с кошельком.\n\n' \
           f'➕ Найдите недоработку/ошибку - сообщите в <a href="https://t.me/LiteWalletSupportRobot">техническую поддержку </a>' \
           '<b>и получите 1 LiteCoin</b></i>'
    await message.answer(text=text)

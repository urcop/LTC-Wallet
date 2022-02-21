from aiogram.dispatcher.filters.state import StatesGroup, State


class SellLtc(StatesGroup):
    count = State()


class SupportMsg(StatesGroup):
    message = State()


class SelectPerson(StatesGroup):
    id_or_nik = State()


class BalanceGive(StatesGroup):
    id = State()
    count = State()


class BalanceTake(StatesGroup):
    id = State()
    count = State()


class Answer(StatesGroup):
    message = State()

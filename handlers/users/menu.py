from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, ReplyKeyboardRemove

from data.config import SMART_BULB_TOKEN
from keyboards.default.menu import bulbs_menu, bulb_menu
from keyboards.default.menu import menu
from loader import dp
from miio.yeelight import Yeelight

smart_bulb = None
smart_bulbs = [
    Yeelight(ip='192.168.1.4', token=SMART_BULB_TOKEN),
]


def get_last_bulb():
    return smart_bulbs[-1]


@dp.message_handler(Command("menu"))
async def show_menu(message: Message):
    await message.answer('Выберете умную технику', reply_markup=menu)


@dp.message_handler(Text(equals='Умные лампы'))
async def show_bulbs_menu(message: Message):
    await message.answer('Выберете умную лампу', reply_markup=bulbs_menu)


@dp.message_handler(Text(equals='1'))
async def show_bulb_menu(message: Message):
    global smart_bulb
    smart_bulb = smart_bulbs[int(message.text) - 1]
    await message.answer('Выберете настройку для лампы', reply_markup=bulb_menu)


@dp.message_handler(Text(equals=['Включить']))
async def turn_on_lump(message: Message):
    smart_bulb.on()
    await dp.bot.send_message(message.from_user.id, "Лампа включена")


@dp.message_handler(text=['Выключить'])
async def turn_off_lump(message: Message):
    smart_bulb.off()
    await dp.bot.send_message(message.from_user.id, "Лампа выключена")

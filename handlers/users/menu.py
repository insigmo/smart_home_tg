from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message

from keyboards.default.menu import bulbs_menu, bulb_menu
from keyboards.default.menu import menu
from loader import dp
from utils.devices.smart_bulbs import SmartBulbs

bulb = SmartBulbs()


@dp.message_handler(Command("menu"))
async def show_menu(message: Message):
    await message.answer('Выберете умную технику', reply_markup=menu)


@dp.message_handler(Text(equals='Умные лампы'))
async def show_bulbs_menu(message: Message):
    print(bulb.bulbs)
    await message.answer('Выберете умную лампу', reply_markup=bulbs_menu)


@dp.message_handler(Text(equals='1'))
async def show_bulb_menu(message: Message):
    bulb.bulb_number = int(message.text) - 1
    await message.answer('Выберете настройку для лампы', reply_markup=bulb_menu)


@dp.message_handler(Text(equals=['Включить']))
async def turn_on_lump(message: Message):
    bulb.turn_on()
    await dp.bot.send_message(message.from_user.id, "Лампа включена")


@dp.message_handler(text=['Выключить'])
async def turn_off_lump(message: Message):
    bulb.turn_off()
    await dp.bot.send_message(message.from_user.id, "Лампа выключена")

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Умные лампы'),
        ],
    ], resize_keyboard=True
)

bulbs_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='1')
        ],
    ], resize_keyboard=True
)


bulb_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Включить'),
            KeyboardButton(text='Выключить')],
    ], resize_keyboard=True
)

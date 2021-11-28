from aiogram import Dispatcher

from data.config import Variables
from utils.misc.logging import logger


async def on_startup_notify(dp: Dispatcher):
    try:
        await dp.bot.send_message(Variables.admin, "Бот Запущен")

    except Exception as err:
        logger.exception(err)

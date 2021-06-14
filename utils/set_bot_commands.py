from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("start", "Start bot"),
            types.BotCommand("menu", "Smart Home Menu"),
            types.BotCommand("help", "Help support"),
        ]
    )

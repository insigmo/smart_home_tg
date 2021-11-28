import os

from environs import Env

env = Env()
env.read_env()


class Variables:
    bot_token = env("BOT_TOKEN")
    admin = env("ADMIN")
    ip = env("IP")
    smart_bulb_token1 = env('SMART_BULB_TOKEN')

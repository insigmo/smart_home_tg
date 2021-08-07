import os

from environs import Env

env = Env()
env.read_env()


class Variables:
    bot_token = os.environ["BOT_TOKEN"]
    admin = os.environ["ADMIN"]
    ip = os.environ["IP"]
    smart_bulb_token1 = os.environ['SMART_BULB_TOKEN1']


from miio import Yeelight

from utils.modules.str_enum import StrEnum


class YeelightTableParams(StrEnum):
    IP = 'ip'
    NAME = 'name'
    DEVICE_TYPE = 'device_type'
    TOKEN = 'token'


class Devices(StrEnum):
    YEELIGHT = 'yeelight', Yeelight, YeelightTableParams

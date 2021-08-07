from utils.constants.devices import Devices
from utils.db_api.db_manager import DBManager


class SmartBulbs:
    def __init__(self):
        self.db_manager = DBManager()
        self.device_type = 'smart_bulb'
        self.bulb_number = 0

    @property
    def bulbs(self):
        devices = filter(lambda x: x.device_type == 'smart_bulb', self.db_manager.device_list)
        bulb_list = []

        for d in devices:
            device = Devices(d.name).additional_fields[0]
            bulb_list.append(device(ip=d.ip, token=d.token))

        return bulb_list

    def add_bulb(self, ip_address: str, token: str, device: Devices = Devices.YEELIGHT):
        self.db_manager.add_device(device, ip=ip_address, token=token, device_type=self.device_type)
        device = device.value()
        self.bulbs.append(device)

    def turn_on(self, bulb_number: int = None):
        bulb_number = bulb_number if bulb_number else self.bulb_number
        self.bulbs[bulb_number].on()

    def turn_off(self, bulb_number: int = None):
        bulb_number = bulb_number if bulb_number else self.bulb_number
        self.bulbs[bulb_number].off()

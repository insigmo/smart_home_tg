import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from data.config import Variables
from utils.constants.devices import Devices
from utils.db_api.tables import Base, DeviceTable


class DBManager:
    def __init__(self):
        self.db_file_path = f'{Variables.root_dir}/data/device_data.db'
        self.engine = create_engine(f'sqlite:///{self.db_file_path}')
        self.session = None
        self._create_session()

    def _create_session(self):
        if os.path.exists(self.db_file_path):
            Base.metadata.bind = self.engine
        else:
            Base.metadata.create_all(self.engine)

        self.session = sessionmaker(bind=self.engine)()

    def add_device(self, device: Devices, **kwargs):
        name = device.value
        params = device.additional_fields[1]
        assert not(set(kwargs.keys()) - set(params)), f'Unknown params {kwargs}'

        ip = kwargs.pop('ip', None)
        device_type = kwargs.pop('device_type', None)
        token = kwargs.pop('token', None)

        device = DeviceTable(ip=ip, name=name, device_type=device_type, token=token)
        self.session.add(device)
        self.save_requests()

    @property
    def device_list(self):
        return self.session.query(DeviceTable).all()

    def save_requests(self):
        self.session.flush()
        self.session.commit()

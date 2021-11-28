
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DeviceTable(Base):
    __tablename__ = 'devices'

    ip = Column(String(250), primary_key=True)
    name = Column(String(250), nullable=False)
    device_type = Column(String(250), nullable=False)
    token = Column(String(250), nullable=False)

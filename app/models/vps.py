from sqlalchemy import Column, Integer, String

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class VPS(Base):

    __tablename__ = 'vps'

    vps_id = Column(Integer, primary_key=True)
    ip_address = Column(String(50))

    def __init__(self, ip_address):
        self.ip_address = ip_address

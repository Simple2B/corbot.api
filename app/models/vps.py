from sqlalchemy import Column, Integer, String

from app import db


class VPS(db.Model):

    __tablename__ = 'vps'

    vps_id = Column(Integer, primary_key=True)
    ip_address = Column(String(50))

    def __init__(self, ip_address):
        self.ip_address = ip_address

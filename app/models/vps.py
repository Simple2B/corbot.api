from app import db
from app.models.utils import ModelMixin


class VPS(db.Model, ModelMixin):

    __tablename__ = 'vps'

    vps_id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(20), nullable=False)

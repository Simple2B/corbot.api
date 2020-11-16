import os
from sqlalchemy import create_engine, MetaData, Column, Integer, String, Table

from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from app.models.vps import VPS


load_dotenv()


DB_IP = os.environ.get("DB_IP", "<NONE>")
DB_NAME = os.environ.get("DB_NAME", "<NONE>")
DB_USER = os.environ.get("DB_USER", "<NONE>")
DB_PASS = os.environ.get("DB_PASS", "<NONE>")
DB_PORT = os.environ.get("DB_PORT", "<NONE>")


class DB1:

    def __init__(self):
        engine_str = (
            "mysql+pymysql://"
            + DB_USER
            + ":"
            + DB_PASS
            + "@"
            + DB_IP
            + ":" + DB_PORT
            + "/"
            + DB_NAME
        )
        engine = create_engine(
            engine_str, pool_size=10, max_overflow=10, pool_recycle=3600
        )
        # Settings
        conn = engine.connect()
        self.metadata = MetaData(bind=engine)
        Session = sessionmaker(bind=conn)
        self.session = Session()


class DB_TEST:

    def __init__(self):
        engine = create_engine('sqlite:///:memory:')
        # You probably need to create some tables and
        # load some test data, do so here.

        # To create tables, you typically do:

        # model.metadata.create_all(engine)
        # Settings
        conn = engine.connect()
        self.metadata = MetaData(bind=engine)
        Table(
            'vps', self.metadata,
            Column('vps_id', Integer, primary_key=True),
            Column('ip_address', String),
        )

        self.metadata.create_all(engine)
        Session = sessionmaker(bind=conn)
        self.session = Session()
        for i in range(9):
            string = '192.0.0.' + str(i)
            u = VPS(string)
            self.session.add(u)
        self.session.commit()

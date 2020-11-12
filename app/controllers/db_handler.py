import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


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

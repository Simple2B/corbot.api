from sqlalchemy import text, Table

from app import db
from app.controllers.register import Register

runner = Register("Runner")


@runner.register()
def service_ident(data):
    msg_subject = data['msg_subject']
    subject = str(msg_subject)
    subject = subject.lower().strip()

    sql = text(f"SELECT svc_name from svc_keys WHERE svc_phrases LIKE '%{subject}%'")
    res = db.engine.execute(sql)
    return res.first()[0]


@runner.register(name="service_ident_v1")
def service_ident_1(data):
    subject = data['msg_subject']

    svc_keys = Table("svc_keys", db.metadata, autoload=True, autoload_with=db.engine)
    qry = svc_keys.select()
    res = db.engine.connect().execute(qry).fetchall()

    svc_requested = "unknown"

    for svc_row in res:
        svc_data = dict(svc_row)
        svc_name = svc_data["svc_name"]
        svc_phrases = svc_data["svc_phrases"]
        pos1 = svc_phrases.find(subject)
        if pos1 >= 0:
            svc_requested = svc_name
            break
    return svc_requested


@runner.register(name="service_ident_v2")
def service_ident_2(data):
    subject = data['msg_subject']

    svc_keys = Table("svc_keys", db.metadata, autoload=True, autoload_with=db.engine)
    qry = svc_keys.select()

    svc_requested = "unknown"
    with db.engine.connect() as conn:
        res = conn.execute(qry).fetchall()

        for svc_row in res:
            svc_data = dict(svc_row)
            svc_name = svc_data["svc_name"]
            svc_phrases = svc_data["svc_phrases"]
            pos1 = svc_phrases.find(subject)
            if pos1 >= 0:
                svc_requested = svc_name
                break
    return svc_requested


@runner.register(name="service_ident_v3")
def service_ident_3(data):
    subject = data['msg_subject']

    svc_keys = Table("svc_keys", db.metadata, autoload=True, autoload_with=db.engine)
    qry = svc_keys.select().where(svc_keys.c.svc_phrases.contains(subject))

    with db.engine.connect() as conn:
        res = conn.execute(qry).fetchall()
        if res:
            return dict(res[0])["svc_name"]
    return "unknown"


@runner.register()
def get_page_limit(data):
    plan_id = data['plan_id']
    sql = text(f"SELECT page_cnt from plans WHERE plan_id={plan_id}")
    res = db.engine.execute(sql)
    row = res.first()
    if not row:
        return None
    page_limit = row[0]
    return page_limit


@runner.register()
def get_client(data):
    client_id = data['client_id']
    sql = text(f"SELECT * from clients WHERE client_id={client_id}")
    res = db.engine.execute(sql)
    row = res.first()
    if not row:
        return None
    client_data = dict(row)
    return client_data

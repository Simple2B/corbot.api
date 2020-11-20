from sqlalchemy import text

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

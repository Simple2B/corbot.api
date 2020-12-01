import datetime
from sqlalchemy import Table

from app import db
from app.controllers.register import Register
from app.logger import log

runner = Register("Runner")


@runner.register(name="service_ident")
def service_ident(data):
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
    plans = Table("plans", db.metadata, autoload=True, autoload_with=db.engine)
    qry = plans.select().where(plans.c.plan_id == plan_id)
    with db.engine.connect() as conn:
        row = conn.execute(qry).first()
    if not row:
        return None
    plan_data = dict(row)
    page_limit = plan_data["page_cnt"]
    return page_limit


@runner.register()
def get_client(data):
    client_id = data['client_id']
    clients = Table("clients", db.metadata, autoload=True, autoload_with=db.engine)
    qry = clients.select().where(clients.c.client_id == client_id)
    with db.engine.connect() as conn:
        row = conn.execute(qry).first()
    if not row:
        return None
    client_data = dict(row)
    return client_data


@runner.register()
def send_msgs(data):
    page_limit = data['page_limit']
    out_msg_list = data['out_msg_list']

    spin_cnt = 0
    for msg_data in out_msg_list:
        if spin_cnt == 0:
            # If first page of message, update existing message
            # Update with Page 1
            upd_out_msg(data)
        else:
            # If not first page of message, enter new message
            if spin_cnt <= page_limit:
                insert_outbound(data)
            else:
                log.debug("Skipping Page: Over " + str(page_limit) + " Count")
        spin_cnt += 1


@runner.register()
def log_run_end(data):
    log_name = data['log_name']
    msg_in = data['msg_in']
    msg_out = data['msg_out']
    start_time = datetime.datetime.strptime(data['start_time'][0], data['start_time'][1])
    end_time = datetime.datetime.now()
    proc_secs = end_time - start_time
    proc_secs = int(proc_secs.total_seconds())
    log_runs = Table("log_api", db.metadata, autoload=True, autoload_with=db.engine)
    i = log_runs.insert()
    i = i.values(
        {
            "log_name": log_name,
            "run_start": start_time,
            "run_end": end_time,
            "msg_rec": msg_in,
            "msg_sent": msg_out,
            "proc_secs": proc_secs,
        }
    )
    with db.engine.connect() as conn:
        conn.execute(i)
    return proc_secs


@runner.register()
def msgs_to_proc(data):
    node_id = data['node_id']
    msg_outbound = Table("msg_outbound", db.metadata, autoload=True, autoload_with=db.engine)
    qry = (
            msg_outbound.select()
            .where(msg_outbound.c.cl_date == None)
            .where(msg_outbound.c.cb_date == None)
            .where(msg_outbound.c.node_id == node_id)
        )
    with db.engine.connect() as conn:
        res = conn.execute(qry)
    msg_list = []
    for row in res:
        msg_data = dict(row)
        msg_list.append(msg_data)
    return msg_list


@runner.register()
def fail_msg(data):
    msg_out_id = data['msg_out_id']
    msg_outbound = Table("msg_outbound", db.metadata, autoload=True, autoload_with=db.engine)
    upd = (
        msg_outbound.update()
        .values(failed=True)
        .where(msg_outbound.c.msg_out_id == msg_out_id)
    )
    with db.engine.connect() as conn:
        conn.execute(upd)


@runner.register()
def upd_out_msg(data):
    msg_out_id = data['msg_out_id']
    new_subject = data['subject']
    new_message = data['new_message']
    new_stamp = datetime.datetime.now()
    msg_outbound = Table("msg_outbound", db.metadata, autoload=True, autoload_with=db.engine)
    upd = (
        msg_outbound.update()
        .values(
            subject=new_subject, message=new_message, routed=1, cb_date=new_stamp
        )
        .where(msg_outbound.c.msg_out_id == msg_out_id)
    )
    with db.engine.connect() as conn:
        conn.execute(upd)


@runner.register()
def insert_outbound(data):
    msg_in_id = data['msg_in_id']
    node_id = data['node_id']
    reg_num = data['reg_num']
    subject = data['subject']
    message = data['message']

    stamp = datetime.datetime.now()
    msg_out = Table("msg_outbound", db.metadata, autoload=True, autoload_with=db.engine)
    i = msg_out.insert()
    i = i.values(
        {
            "msg_in_id": msg_in_id,
            "node_id": node_id,
            "reg_num": reg_num,
            "subject": subject,
            "message": message,
            "cb_date": stamp,
        }
    )
    with db.engine.connect() as conn:
        conn.execute(i)

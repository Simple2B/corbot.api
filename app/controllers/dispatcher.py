
from sqlalchemy import Table

from app import metadata


def api_sum_example(data: dict) -> dict:
    res = int(data['first_argument']) + int(data['second_argument'])
    return res


def api_sum_array_example(data: dict) -> dict:
    res = sum(data)
    return res


def service_ident(data):
    msg_subject = data['msg_subject']
    subject = str(msg_subject)
    subject = subject.lower().strip()
    svc_keys = Table("svc_keys", metadata, autoload=True)
    qry = svc_keys.select()
    res = qry.execute()
    svc_requested = "unknown"
    for svc_row in res:
        svc_data = dict(svc_row)
        svc_name = svc_data["svc_name"]
        svc_phrases = svc_data["svc_phrases"]
        pos1 = svc_phrases.find(subject)
        if pos1 >= 0:
            svc_requested = svc_name
    return svc_requested


def get_page_limit(data):
    plan_id = data['plan_id']
    plans = Table("plans", metadata, autoload=True)
    qry = plans.select().where(plans.c.plan_id == plan_id)
    res = qry.execute()
    for row in res:
        plan_data = dict(row)
    page_limit = plan_data["page_cnt"]
    return page_limit


def get_client(data):
    client_id = data['client_id']
    clients = Table("clients", metadata, autoload=True)
    qry = clients.select().where(clients.c.client_id == client_id).limit(1)
    res = qry.execute()
    client_data = {}
    for row in res:
        client_data = dict(row)
    return client_data


def dispatch(request_data: dict):
    method_name = request_data["request"]
    if method_name in MAP:
        if "data" not in request_data:
            # abort("Unknown method")
            pass
        method = MAP[method_name]
        # res_to_json converts function responce to standart format
        return dict(request=method_name, data=method(request_data["data"]))


MAP = {
    "get_page_limit": get_page_limit,
    'sum': api_sum_example,
    'service_ident': service_ident,
    'array': api_sum_array_example,
    'get_page_limit': get_page_limit,
    'get_client': get_client,
}


from sqlalchemy import Table

from app import session, metadata


def get_page_limit(data: dict) -> dict:
    pass


def api_sum_example(data: dict) -> dict:
    res = int(data['first_argument']) + int(data['second_argument'])
    return {"res": res}


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
    return {'svc_requested': svc_requested}


MAP = {
    "get_page_limit": get_page_limit,
    'sum': api_sum_example,
    'service_ident': service_ident,
}


def dispatch(request_data: dict):
    method_name = request_data["request"]
    if method_name in MAP:
        if "data" not in request_data:
            # abort("Unknown method")
            pass
        method = MAP[method_name]
        return method(request_data["data"])

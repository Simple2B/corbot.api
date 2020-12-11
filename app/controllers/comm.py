from datetime import date, timedelta

from .runner import Runner


def comm(client_id):
    now = date.today()
    expire_date = Runner.get_client(client_id)['expire_date']
    expired = 1
    if expire_date - now > timedelta(0):
        expired = 0
    return expired

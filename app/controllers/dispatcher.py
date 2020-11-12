
def get_page_limit(data: dict) -> dict:
    pass


def api_sum_example(data: dict) -> dict:
    res = int(data['first_argument']) + int(data['second_argument'])
    return {"res": res}


MAP = {
    "get_page_limit": get_page_limit,
    'sum': api_sum_example,
}


def dispatch(request_data: dict):
    method_name = request_data["request"]
    if method_name in MAP:
        if "data" not in request_data:
            # abort("Unknown method")
            pass
        method = MAP[method_name]
        return method(request_data["data"])

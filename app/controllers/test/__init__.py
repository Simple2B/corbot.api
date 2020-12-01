from app.controllers.register import Register

test = Register("Test")


@test.register(name="sum")
def api_sum_example(data: dict) -> dict:
    res = int(data['a']) + int(data['b'])
    return res


@test.register(name="sum_app")
def api_sum_array_example(data: dict) -> dict:
    res = sum(data)
    return res

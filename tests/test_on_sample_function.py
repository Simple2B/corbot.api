import json

import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app(environment="testing")
    app.config["TESTING"] = True

    with app.test_client() as client:
        app_ctx = app.app_context()
        app_ctx.push()
        yield client
        app_ctx.pop()


def test_on_sample_function(client):
    first_argument = 56
    second_argument = 34
    request_dict = {
        "request": "sum",
        "data": {
            "first_argument": first_argument,
            "second_argument": second_argument
        }
    }
    json_data = json.dumps(request_dict)
    response = client.post('/api', json=json_data)
    assert response.status_code == 200
    assert json.loads(response.data)['array_res'][0] == 90

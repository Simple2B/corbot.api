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


def test_wrong_function(client):
    first_argument = 56
    second_argument = 34
    request_dict = {
        "request": "sun",
        "data": {
            "first_argument": first_argument,
            "second_argument": second_argument
        }
    }
    response = client.post('/api', json=request_dict)
    assert response.json['error'] == 'The method [sun] is not registered'
    assert response.status_code == 400


def test_wrong_argument(client):
    first_argument = 56
    second_argument = 'qwe'
    request_dict = {
        "request": "sum",
        "data": {
            "first_argument": first_argument,
            "second_argument": second_argument
        }
    }
    response = client.post('/api', json=request_dict)
    assert 'Inappropriate argument' in response.json['doc']
    assert response.status_code == 400


def test_missing_argument(client):
    first_argument = 56
    request_dict = {
        "request": "sum",
        "data": {
            "first_argument": first_argument
        }
    }
    response = client.post('/api', json=request_dict)
    assert 'Mapping key not found.' in response.json['doc']
    assert response.status_code == 400

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
    response = client.post('/api', json=request_dict)
    assert response.status_code == 200
    assert int(response.json['data']) == first_argument + second_argument  # checking that right response was returned


def test_service_ident(client):
    response = client.post('/api', json={
        "request": "service_ident",
        "data": {
            "msg_subject": "help"
        }
    })
    assert response.status_code == 200
    assert response.json
    assert "data" in response.json
    assert response.json["data"] == "Support"
    # version 1
    response = client.post('/api', json={
        "request": "service_ident_v1",
        "data": {
            "msg_subject": "help"
        }
    })
    assert response.status_code == 200
    assert response.json
    assert "data" in response.json
    assert response.json["data"] == "Support"
    # version 2
    response = client.post('/api', json={
        "request": "service_ident_v2",
        "data": {
            "msg_subject": "help"
        }
    })
    assert response.status_code == 200
    assert response.json
    assert "data" in response.json
    assert response.json["data"] == "Support"
    # version 3
    response = client.post('/api', json={
        "request": "service_ident_v3",
        "data": {
            "msg_subject": "help"
        }
    })
    assert response.status_code == 200
    assert response.json
    assert "data" in response.json
    assert response.json["data"] == "Support"


def test_get_client(client):
    response = client.post('/api', json={
        "request": "get_client",
        "data": {
            "client_id": 30
        }
    })
    assert response.status_code == 200
    assert response.json
    assert "data" in response.json
    assert "age" in response.json["data"]

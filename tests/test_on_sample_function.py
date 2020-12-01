import datetime

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
            "a": first_argument,
            "b": second_argument
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


def test_get_client(client):
    response = client.post('/api', json={
        "request": "get_client",
        "data": {
            "client_id": 30
        }
    })
    assert response.status_code == 200, response.json
    assert response.json
    assert "data" in response.json
    assert "age" in response.json["data"]


def test_get_page_limit(client):
    response = client.post('/api', json={
        "request": "get_page_limit",
        "data": {
            "plan_id": 4
        }
    })
    assert response.status_code == 200
    assert response.json
    assert "data" in response.json
    assert response.json["data"] == 5


def test_log_run_end(client):
    response = client.post('/api', json={
        "request": "log_run_end",
        "data": {
            "log_name": 'fireName',
            "msg_in": 1,
            "msg_out": 2,
            "start_time": ('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p'),
        }
    })
    assert response.status_code == 200
    assert response.json
    assert "data" in response.json


def test_msgs_to_proc(client):
    response = client.post('/api', json={
        "request": "msgs_to_proc",
        "data": {
            "node_id": 1309,
        }
    })
    assert response.status_code == 200
    assert response.json
    assert "data" in response.json


def test_fail_msg(client):
    response = client.post('/api', json={
        "request": "fail_msg",
        "data": {
            "msg_out_id": 1593191,
        }
    })
    assert response.status_code == 200
    assert response.json
    assert "data" in response.json


def test_upd_out_msg(client):
    response = client.post('/api', json={
        "request": "upd_out_msg",
        "data": {
            "msg_out_id": 1593191,
            "subject": 'Link',
            "new_message": 'non5',
        }
    })
    assert response.status_code == 200
    assert response.json
    assert "data" in response.json


def test_insert_outbound(client):
    response = client.post('/api', json={
        "request": "insert_outbound",
        "data": {
            "msg_in_id": 0,
            "node_id": 203,
            "reg_num": '13262021',
            "subject": 'Link',
            "message": "jpfi",
        }
    })
    assert response.status_code == 200
    assert response.json
    assert "data" in response.json


def test_send_msgs(client):
    response = client.post('/api', json={
        "request": "send_msgs",
        "data": {
            "msg_in_id": 0,
            "node_id": 203,
            "reg_num": '13262021',
            "message": "jpfi",
            "msg_out_id": 1593191,
            "subject": 'Link',
            "new_message": 'non5',
            "client_id": 33,
            "page_limit": 9,
            "out_msg_list": [1, 2, 3],
        }
    })
    assert response.status_code == 200
    assert response.json
    assert "data" in response.json

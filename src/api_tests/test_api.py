'''
Tests for data validation.

Author: Dauren Baitursyn
Date: 26.08.22
'''
import json

from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)


def test_greeting():
    r = client.get('/')
    assert r.status_code == 200, ''
    assert r.json()['message'] == (
        'To test, please, send `POST` request with data on the person '
        'to `/persons/` to get prediction on the salary.')


def test_persons_true(data_true):
    data = json.dumps(data_true)
    r = client.post('/persons/', data=data)
    assert r.status_code == 200
    assert r.json()['prediction'] == '>50K'


def test_persons_false(data_false):
    data = json.dumps(data_false)
    r = client.post('/persons/', data=data)
    assert r.status_code == 200
    assert r.json()['prediction'] == '<=50K'


def test_persons_valid(data_valid):
    for data, msg in data_valid:
        data = json.dumps(data)
        r = client.post('/persons/', data=data)
        assert r.status_code == 200, msg
        assert r.json()['prediction'] in ('>50K, <=50K'), msg


def test_persons_invalid(data_invalid):
    for data, msg in data_invalid:
        print(data)
        data = json.dumps(data)
        r = client.post('/persons/', data=data)
        assert r.status_code == 422, msg

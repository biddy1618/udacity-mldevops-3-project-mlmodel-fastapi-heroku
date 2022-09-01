'''
'''
import json

from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)


def test_greeting():
    r = client.get('/')
    assert r.status_code == 200
    assert r.json()['info'] == (
        'To test, please, send `POST` request '
        'with data on the person...')


def test_persons():
    data = json.dumps({})
    r = client.post('/persons/', data=data)
    assert r.status_code == 200
    assert r.json()['Prediction'] == 0

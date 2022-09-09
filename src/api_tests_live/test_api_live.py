'''
Module for testing live API.

Author: Dauren Baitursyn
Date: 07.09.22
'''
import requests
import json
import urllib.parse

URL_TO_TEST = 'https://dauren-test-project.herokuapp.com/'


def test_greeting():
    r = requests.get(URL_TO_TEST)
    assert r.status_code == 200, ''
    assert r.json()['message'] == (
        'To test, please, send `POST` request with data on the person '
        'to `/persons/` to get prediction on the salary.')


def test_persons_true(data_true):
    data = json.dumps(data_true)
    r = requests.post('/persons/', data=data)
    assert r.status_code == 200
    assert r.json()['prediction'] == '>50K'


def test_persons_false(data_false):
    data = json.dumps(data_false)
    r = requests.post('/persons/', data=data)
    assert r.status_code == 200
    assert r.json()['prediction'] == '<=50K'


def test_persons_valid(data_valid):
    for data, msg in data_valid:
        data = json.dumps(data)
        r = requests.post(
            urllib.parse.urljoin(URL_TO_TEST, 'persons'), data=data)
        assert r.status_code == 200, msg
        assert r.json()['prediction'] in ('>50K, <=50K'), msg


def test_persons_invalid(data_invalid):
    for data, msg in data_invalid:
        print(data)
        data = json.dumps(data)
        r = requests.post(
            urllib.parse.urljoin(URL_TO_TEST, 'persons'), data=data)
        assert r.status_code == 422, msg

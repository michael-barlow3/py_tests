import http
import os
import json
import pytest
from wtf import APP

ROUTE = '/slack'
TEST_TOKENS = ['token1', 'token2']

@pytest.fixture
def client():
    client = APP.test_client()
    APP.config['TESTING'] = True
    APP.config['SLACK_TOKENS'] = TEST_TOKENS
    yield client

def test_env_vars_present():
    for var in ['SLACK_TOKENS', 'DATA_URL']:
        assert os.getenv(var) != None

@pytest.mark.parametrize("token", TEST_TOKENS)
def test_good_payload_using_valid_token(client, token):
    data = {'text': 'vba','token': token}
    r = client.post(ROUTE, data=data)
    assert b'Veterans Benefits Administration' in r.data
    assert r.status_code == http.HTTPStatus.OK

def test_multi_def_payload(client):
    data = {'text': 'aaa','token': TEST_TOKENS[0]}
    r = client.post(ROUTE, data=data)
    assert b' - Abdominal Aortic Aneurysm;' in r.data
    assert b' - Area Agencies on Aging;' in r.data

# def test_context_payload(client):
#     data = {'text': '3pao','token': TEST_TOKENS[0]}
#     r = client.post(ROUTE, data=data)
#     # print (r.data)
#     assert b'3pao\n - Third Party Assessment Organization\n\t- FedRAMP requires a 3PA0 to verify the attestations made in an SSP' in r.data

# def test_note_payload(client):
#     data = {'text': 'ahlta','token': TEST_TOKENS[0]}
#     r = client.post(ROUTE, data=data)
#     assert b'ahlta\n - Armed Forces Health Longitudinal Technology Application\n\t- DoD electronic medical record system' in r.data    

# def test_comma_in_def(client):
#     data = {'text': 'acre','token': TEST_TOKENS[0]}
#     r = client.post(ROUTE, data=data)
#     assert b'A measure of land 43,560 sq. ft.' in r.data

# def test_bad_payload(client):
#     data = {'foo': 'bar', 'token': TEST_TOKENS[0]}
#     r = client.post(ROUTE, data=data)
#     assert b'Improper request' in r.data
#     assert r.status_code == http.HTTPStatus.BAD_REQUEST

# def test_no_slack_token(client):
#     data = {'text': 'vba','token': 'foobar'}
#     r = client.post(ROUTE, data=data)
#     assert b'Not authorized' in r.data
#     assert r.status_code == http.HTTPStatus.UNAUTHORIZED

# def test_not_found(client):
#     data = {'text': '13231312334','token': TEST_TOKENS[0]}
#     r = client.post(ROUTE, data=data)
#     assert b'not found!' in r.data
#     assert b'13231312334' in r.data
#     assert r.status_code == http.HTTPStatus.OK

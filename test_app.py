#!/usr/bin/python3
 
import os
import tempfile
 
import pytest
 
from app import APP
 
@pytest.fixture
def client():
    APP.config['TESTING'] = True
    client = APP.test_client()
 
    yield client
 
def test_valid_transaction(client):
    card = {
            "status": True,
            "number":123456,
            "limit":1000,
            "transaction":{
                "amount":500
            }
        }
    rv = client.post("/api/transaction",json=card)    
    assert  True == rv.get_json().get("approved")    
    assert  500 == rv.get_json().get("newLimit")
 
def test_above_limit(client):
    card = {
            "status": True,
            "number":123456,
            "limit":1000,
            "transaction":{
                "amount":1500
            }
        }
    rv = client.post("/api/transaction",json=card)    
    assert  False == rv.get_json().get("approved")
    assert  "Transaction above the limit" in rv.get_json().get("reason")
 
def test_blocked_card(client):
    card = {
            "status": False,
            "number":123456,
            "limit":1000,
            "transaction":{
                "amount":500
            }
        }
    rv = client.post("/api/transaction",json=card)    
    assert  False == rv.get_json().get("approved")
    assert  "Blocked Card" in rv.get_json().get("reason")

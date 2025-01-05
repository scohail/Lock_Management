#test_basic_operations.py
import pytest
from client.client import HDFSClient

@pytest.fixture
def client():
    return HDFSClient()

def test_health_check(client):
    response = client.health_check()
    assert response['status'] == 'healthy'

def test_write_and_read(client):
    # Test write
    write_response = client.write_data('test_key', 'test_value')
    assert 'message' in write_response
    
    # Test read
    read_response = client.read_data('test_key')
    assert read_response['value'] == 'test_value'
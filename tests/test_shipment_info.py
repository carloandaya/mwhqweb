import pytest
from mywireless.db import get_db_raw


def test_index(client):
    response = client.get('/shipment_info')
    assert b'Shipment Information' in response.data
    assert b'Shipped Not Received' in response.data
    assert b'Delivered Not Received' in response.data

import pytest
from mywireless.db import get_db_raw


def test_index(client):
    response = client.get('/shipment_info')
    assert b'Shipment Information' in response.data
    assert b'Shipped Not Received' in response.data
    assert b'Delivered Not Received' in response.data
    assert b'Shipped Not Delivered' in response.data


def test_shipped_not_received(client, app):
    response = client.get('/shipment_info/shipped_not_received')
    assert b'Shipped Not Received' in response.data
    assert b'358711099663452' in response.data
    assert b'354834099171450' in response.data
    assert b'356172099533090' in response.data
    assert b'353094104750878' in response.data

    with app.app_context():
        db = get_db_raw()
        count = db.execute('SELECT COUNT(IMEI)'
                           ' FROM ATT_ShipmentDetailReport'
                           ' WHERE IsReceived = ?', 0).fetchone()[0]
        assert count == 4


def test_shipped_not_delivered(client, app):
    response = client.get('/shipment_info/shipped_not_delivered')
    assert b'Shipped Not Delivered' in response.data
    assert b'358711099663452' not in response.data
    assert b'354834099171450' not in response.data
    assert b'356172099533090' in response.data
    assert b'353094104750878' in response.data


def test_delivered_not_received(client, app):
    response = client.get('/shipment_info/delivered_not_received')
    assert b'Delivered Not Received' in response.data
    assert b'358711099663452' in response.data
    assert b'354834099171450' in response.data
    assert b'356172099533090' not in response.data
    assert b'353094104750878' not in response.data

    with app.app_context():
        db = get_db_raw()
        count = db.execute('SELECT COUNT(IMEI)'
                           ' FROM ATT_ShipmentDetailReport'
                           ' WHERE IsReceived = ? AND DeliveryStatus = ?', (0, 'D')).fetchone()[0]
        assert count == 2

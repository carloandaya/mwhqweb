import pytest
from mywireless.db import get_db_raw


def test_index(client):
    response = client.get('/shipment-info')
    assert b'Shipment Information' in response.data
    assert b'Shipped Not Received' in response.data
    assert b'Delivered Not Received' in response.data
    assert b'Shipped Not Delivered' in response.data


def test_shipped_not_received(client, app):
    response = client.get('/shipment-info/shipped-not-received')
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
    response = client.get('/shipment-info/shipped-not-delivered')
    assert b'Shipped Not Delivered' in response.data
    assert b'358711099663452' not in response.data
    assert b'354834099171450' not in response.data
    assert b'356172099533090' in response.data
    assert b'353094104750878' in response.data


def test_delivered_not_received(client, app):
    response = client.get('/shipment-info/delivered-not-received')
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


def test_update_by_imei(client, app):
    assert client.get('/shipment-info/imei/358711099663452/update').status_code == 200
    assert client.get('/shipment-info/imei/1/update').status_code == 404

    client.post('/shipment-info/imei/358711099663452/update', data={'delivery_status': 'D', 'is_received': 'received'})
    with app.app_context():
        db = get_db_raw()
        shipment = db.execute('SELECT DeliveryStatus, IsReceived'
                              ' FROM ATT_ShipmentDetailReport'
                              ' WHERE IMEI = ?', '358711099663452').fetchone()
        assert shipment[0] == 'D'
        assert shipment[1]

    client.post('/shipment-info/imei/358711099663452/update', data={'delivery_status': '', 'is_received': 'received'})
    with app.app_context():
        db = get_db_raw()
        shipment = db.execute('SELECT DeliveryStatus, IsReceived'
                              ' FROM ATT_ShipmentDetailReport'
                              ' WHERE IMEI = ?', '358711099663452').fetchone()
        assert not shipment[0]
        assert shipment[1]

    client.post('/shipment-info/imei/358711099663452/update', data={'delivery_status': ''})
    with app.app_context():
        db = get_db_raw()
        shipment = db.execute('SELECT DeliveryStatus, IsReceived'
                              ' FROM ATT_ShipmentDetailReport'
                              ' WHERE IMEI = ?', '358711099663452').fetchone()
        assert not shipment[0]
        assert not shipment[1]

    client.post('/shipment-info/imei/358711099663452/update', data={'delivery_status': 'D'})
    with app.app_context():
        db = get_db_raw()
        shipment = db.execute('SELECT DeliveryStatus, IsReceived'
                              ' FROM ATT_ShipmentDetailReport'
                              ' WHERE IMEI = ?', '358711099663452').fetchone()
        assert shipment[0] == 'D'
        assert not shipment[1]

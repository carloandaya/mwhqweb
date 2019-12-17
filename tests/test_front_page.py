def test_index(client):
    response = client.get('/')
    assert b'Data Warehouse' in response.data
    assert b'Shipment Information' in response.data
    assert b'Human Resources' in response.data


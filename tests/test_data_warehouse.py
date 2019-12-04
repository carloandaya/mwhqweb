import pytest
from mywireless.db import get_db


def test_categories_index(client):
    response = client.get('/data_warehouse/categories')
    assert b'Phone' in response.data
    assert b'Accessory' in response.data


def test_categories_create(client, app):
    assert client.get('/data_warehouse/categories/create').status_code == 200

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(CategoryKey) FROM DimCategory').fetchone()[0]
        assert count == 2


def test_categories_update(client, app):
    assert client.get('/data_warehouse/categories/1/update').status_code == 200
    assert client.get('/data_warehouse/categories/3/update').status_code == 404

    client.post('/data_warehouse/categories/1/update', data={'category_name': 'updated'})
    with app.app_context():
        db = get_db()
        category = db.execute('SELECT CategoryName FROM DimCategory WHERE CategoryKey = 1').fetchone()
        assert category[0] == 'updated'

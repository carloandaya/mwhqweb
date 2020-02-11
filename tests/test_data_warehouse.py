import pytest
from mywireless.db import get_db


def test_index(client):
    response = client.get('/data_warehouse/')
    assert b'Data Warehouse' in response.data
    assert b'Administration' in response.data
    assert b'Categories' in response.data
    assert b'Manufacturers' in response.data
    assert b'Maintenance' in response.data


def test_categories_index(client, app):
    response = client.get('/data_warehouse/categories')
    assert b'Phone' in response.data
    assert b'Accessory' in response.data

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(CategoryKey) FROM DimCategory').fetchone()[0]
        assert count == 2


def test_categories_create(client, app):
    assert client.get('/data_warehouse/categories/create').status_code == 200
    client.post('/data_warehouse/categories/create', data={'category_name': 'New Category'})

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(CategoryKey) FROM DimCategory').fetchone()[0]
        assert count == 3


def test_categories_create_empty(client):
    response = client.post('/data_warehouse/categories/create', data={'category_name': ''})
    assert b'Category Name is required.' in response.data


def test_categories_create_existing(client):
    response = client.post('/data_warehouse/categories/create', data={'category_name': 'Phone'})
    assert b'Category Name Phone already exists.' in response.data


def test_categories_update(client, app):
    assert client.get('/data_warehouse/categories/1/update').status_code == 200
    assert client.get('/data_warehouse/categories/3/update').status_code == 404

    client.post('/data_warehouse/categories/1/update', data={'category_name': 'updated'})
    with app.app_context():
        db = get_db()
        category = db.execute('SELECT CategoryName FROM DimCategory WHERE CategoryKey = 1').fetchone()
        assert category[0] == 'updated'


def test_categories_update_empty(client):
    response = client.post('/data_warehouse/categories/1/update', data={'category_name': ''})
    assert b'Category Name is required.' in response.data


def test_categories_update_existing(client):
    response = client.post('/data_warehouse/categories/1/update', data={'category_name': 'Phone'})
    assert b'Category Name Phone already exists.' in response.data


def test_locations_index(client):
    response = client.get('/data_warehouse/locations')
    assert b'Locations' in response.data
    assert b'Azusa' in response.data
    assert b'CAGLA Market' in response.data


def test_locations_detail(client):
    response = client.get('data_warehouse/locations/1')
    assert b'Azusa' in response.data


def test_locations_create(client, app):
    assert client.get('/data_warehouse/locations/create').status_code == 200
    client.post('/data_warehouse/locations/create', data={'name': 'Test', 'region': 2, 'dealer_code': 'Test',
                                                          'rq_abbreviation': 'Test', 'is_active': 'y'})

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(StoreKey) FROM DimStore').fetchone()[0]
        assert count == 2


def test_locations_update(client, app):
    assert client.get('/data_warehouse/locations/1/update').status_code == 200
    client.post('/data_warehouse/locations/1/update', data={'name': 'AT&T - Fremont', 'region': 2})

    with app.app_context():
        db = get_db()
        store = db.execute('SELECT StoreName FROM DimStore WHERE StoreKey = 1').fetchone()
        assert store.StoreName == 'AT&T - Fremont'


def test_manufacturers_index(client, app):
    response = client.get('/data_warehouse/manufacturers')
    assert b'Apple' in response.data
    assert b'Samsung' in response.data
    assert b'LG Electronics' in response.data
    assert b'Amazon' not in response.data

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(ManufacturerKey) FROM DimManufacturer').fetchone()[0]
        assert count == 4


def test_products_index(client):
    response = client.get('/data_warehouse/products')
    assert b'Apple iPhone 11 Pro Max 512GB Midnight Green' in response.data
    assert b'Apple iPhone 7 32GB Black' in response.data
    assert b'Apple iPhone 7 32GB Silver' in response.data


def test_products_update(client, app):
    assert client.get('/data_warehouse/products/AEDEPB000159/update').status_code == 200
    client.post('/data_warehouse/products/AEDEPB000159/update', data={'product_name': 'Product Update',
                                                                      'manufacturer_key': 1,
                                                                      'category_key': 2,
                                                                      'subcategory_key': 1})

    with app.app_context():
        db = get_db()
        product = db.execute('SELECT ProductName FROM DimProduct WHERE ProductKey = ?', 'AEDEPB000159').fetchone()
        assert product.ProductName == 'Product Update'


def test_products_no_manufacturer(client):
    response = client.get('/data_warehouse/maintenance/products-no-manufacturer')
    assert b'Apple iPhone 7 32GB Silver' in response.data


def test_manufacturers_create(client, app):
    assert client.get('/data_warehouse/manufacturers/create').status_code == 200
    client.post('/data_warehouse/manufacturers/create', data={'manufacturer_name': 'New Manufacturer'})

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(ManufacturerKey) FROM DimManufacturer').fetchone()[0]
        assert count == 5


def test_manufacturers_create_empty(client):
    response = client.post('/data_warehouse/manufacturers/create', data={'manufacturer_name': ''})
    assert b'Manufacturer Name is required.' in response.data


def test_manufacturers_create_existing(client):
    response = client.post('/data_warehouse/manufacturers/create', data={'manufacturer_name': 'Apple'})
    assert b'Manufacturer Name Apple already exists.' in response.data


def test_manufacturers_update(client, app):
    assert client.get('/data_warehouse/manufacturers/1/update').status_code == 200
    assert client.get('/data_warehouse/manufacturers/4/update').status_code == 404

    client.post('/data_warehouse/manufacturers/1/update', data={'manufacturer_name': 'updated'})
    with app.app_context():
        db = get_db()
        category = db.execute('SELECT ManufacturerName FROM DimManufacturer WHERE ManufacturerKey = 1').fetchone()
        assert category[0] == 'updated'


def test_manufacturers_update_empty(client):
    response = client.post('/data_warehouse/manufacturers/1/update', data={'manufacturer_name': ''})
    assert b'Manufacturer Name is required.' in response.data


def test_manufacturers_update_existing(client):
    response = client.post('/data_warehouse/manufacturers/2/update', data={'manufacturer_name': 'Apple'})
    assert b'Manufacturer Name Apple already exists.' in response.data

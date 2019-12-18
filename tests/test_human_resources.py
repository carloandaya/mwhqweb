import pytest
from mywireless.db import get_db


def test_index(client):
    response = client.get('/human_resources')
    assert b'Human Resources' in response.data
    assert b'Administration' in response.data
    assert b'Employees' in response.data


def test_employees_index(client, app):
    response = client.get('/human_resources/employees')
    assert b'Employees' in response.data

#
#     with app.app_context():
#         db = get_db()
#         count = db.execute('SELECT COUNT(CategoryKey) FROM DimCategory').fetchone()[0]
#         assert count == 2
#
#
# def test_categories_create(client, app):
#     assert client.get('/data_warehouse/categories/create').status_code == 200
#     client.post('/data_warehouse/categories/create', data={'category_name': 'New Category'})
#
#     with app.app_context():
#         db = get_db()
#         count = db.execute('SELECT COUNT(CategoryKey) FROM DimCategory').fetchone()[0]
#         assert count == 3
#
#
# def test_categories_create_empty(client):
#     response = client.post('/data_warehouse/categories/create', data={'category_name': ''})
#     assert b'Category Name is required.' in response.data
#
#
# def test_categories_create_existing(client):
#     response = client.post('/data_warehouse/categories/create', data={'category_name': 'Phone'})
#     assert b'Category Name Phone already exists.' in response.data
#
#
# def test_categories_update(client, app):
#     assert client.get('/data_warehouse/categories/1/update').status_code == 200
#     assert client.get('/data_warehouse/categories/3/update').status_code == 404
#
#     client.post('/data_warehouse/categories/1/update', data={'category_name': 'updated'})
#     with app.app_context():
#         db = get_db()
#         category = db.execute('SELECT CategoryName FROM DimCategory WHERE CategoryKey = 1').fetchone()
#         assert category[0] == 'updated'
#
#
# def test_categories_update_empty(client):
#     response = client.post('/data_warehouse/categories/1/update', data={'category_name': ''})
#     assert b'Category Name is required.' in response.data
#
#
# def test_categories_update_existing(client):
#     response = client.post('/data_warehouse/categories/1/update', data={'category_name': 'Phone'})
#     assert b'Category Name Phone already exists.' in response.data
#
#
# def test_manufacturers_index(client, app):
#     response = client.get('/data_warehouse/manufacturers')
#     assert b'Apple' in response.data
#     assert b'Samsung' in response.data
#     assert b'LG Electronics' in response.data
#     assert b'Amazon' not in response.data
#
#     with app.app_context():
#         db = get_db()
#         count = db.execute('SELECT COUNT(ManufacturerKey) FROM DimManufacturer').fetchone()[0]
#         assert count == 3
#
#
# def test_manufacturers_create(client, app):
#     assert client.get('/data_warehouse/manufacturers/create').status_code == 200
#     client.post('/data_warehouse/manufacturers/create', data={'manufacturer_name': 'New Manufacturer'})
#
#     with app.app_context():
#         db = get_db()
#         count = db.execute('SELECT COUNT(ManufacturerKey) FROM DimManufacturer').fetchone()[0]
#         assert count == 4
#
#
# def test_manufacturers_create_empty(client):
#     response = client.post('/data_warehouse/manufacturers/create', data={'manufacturer_name': ''})
#     assert b'Manufacturer Name is required.' in response.data
#
#
# def test_manufacturers_create_existing(client):
#     response = client.post('/data_warehouse/manufacturers/create', data={'manufacturer_name': 'Apple'})
#     assert b'Manufacturer Name Apple already exists.' in response.data
#
#
# def test_manufacturers_update(client, app):
#     assert client.get('/data_warehouse/manufacturers/1/update').status_code == 200
#     assert client.get('/data_warehouse/manufacturers/4/update').status_code == 404
#
#     client.post('/data_warehouse/manufacturers/1/update', data={'manufacturer_name': 'updated'})
#     with app.app_context():
#         db = get_db()
#         category = db.execute('SELECT ManufacturerName FROM DimManufacturer WHERE ManufacturerKey = 1').fetchone()
#         assert category[0] == 'updated'
#
#
# def test_manufacturers_update_empty(client):
#     response = client.post('/data_warehouse/manufacturers/1/update', data={'manufacturer_name': ''})
#     assert b'Manufacturer Name is required.' in response.data
#
#
# def test_manufacturers_update_existing(client):
#     response = client.post('/data_warehouse/manufacturers/2/update', data={'manufacturer_name': 'Apple'})
#     assert b'Manufacturer Name Apple already exists.' in response.data
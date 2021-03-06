import pytest
from flask import g, session, current_app
from mywireless.db import get_db


def test_index(client):
    response = client.get('/human_resources/')
    assert b'Human Resources' in response.data
    assert b'Administration' in response.data
    assert b'Employees' in response.data


def test_employees_index(client, app):
    response = client.get('/human_resources/employees')
    assert b'Employees' in response.data

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(EmployeeKey) FROM DimEmployee').fetchone()[0]
        assert count == 1


def test_employee_detail(client):
    response = client.get('/human_resources/employees/101098')
    assert b'Carlo Andaya' in response.data


def test_employee_does_not_exist(client):
    response = client.get('/human_resources/100000/employee')
    print(response.data)
    assert response.status_code == 404


def test_employee_create(client, app):
    response = client.get('/human_resources/employees/create')
    assert response.status_code == 200

    client.post('human_resources/employees/create', data={'name': 'New User', 'first_name': 'New',
                                                          'last_name': 'User', 'initials': 'NU'})

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(EmployeeKey) FROM DimEmployee').fetchone()[0]
        assert count == 2
        new_user = db.execute('SELECT EmployeeKey, EmployeeName, Email '
                              'FROM DimEmployee WHERE EmployeeKey = ?', 150000).fetchone()
        assert new_user[0] == 150000
        assert new_user[1] == 'New User'
        assert new_user[2] == 'nu150000@mywirelessgroup.com'


def test_employee_update(client, app):
    response = client.get('/human_resources/employees/101098/update')
    assert response.status_code == 200

    client.post('human_resources/employees/101098/update', data={'name': 'Update User',
                                                                 'first_name': 'Update',
                                                                 'last_name': 'User',
                                                                 'att_uid': ''})
    with app.app_context():
        db = get_db()
        employee = db.execute('SELECT EmployeeName, ATTUID, Email '
                              'FROM DimEmployee '
                              'WHERE EmployeeKey = ?',
                              101098).fetchone()
        assert employee.EmployeeName == 'Update User'
        assert employee.ATTUID == ''

    client.post('human_resources/employees/101098/update', data={'name': 'Update User',
                                                                 'first_name': 'Update',
                                                                 'last_name': 'User',
                                                                 'att_uid': 'ca941g'})
    with app.app_context():
        db = get_db()
        employee = db.execute('SELECT EmployeeName, ATTUID, Email '
                              'FROM DimEmployee '
                              'WHERE EmployeeKey = ?',
                              101098).fetchone()
        assert employee.EmployeeName == 'Update User'
        assert employee.ATTUID == 'ca941g'




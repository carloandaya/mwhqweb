import os

import pytest
from mywireless import create_app
from mywireless.db import get_db, init_db


with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'DATABASE': 'DRIVER={SQL Server};SERVER=localhost;DATABASE=Test_MyWirelessDW;Trusted_Connection=yes',
    })

    with app.app_context():
        init_db()
        db = get_db()
        db.execute(_data_sql)
        db.commit()

    yield app


@pytest.fixture
def client(app):
    return app.test_client()

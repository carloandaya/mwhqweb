import pytest
import pyodbc
from mywireless.db import get_db


def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(pyodbc.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e.value)


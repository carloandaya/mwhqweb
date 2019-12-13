import pytest
import pyodbc
from mywireless.db import get_db, get_db_raw


def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(pyodbc.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e.value)

    with app.app_context():
        db_raw = get_db_raw()
        assert db_raw is get_db_raw()

    with pytest.raises(pyodbc.ProgrammingError) as e:
        db_raw.execute('SELECT 1')

    assert 'closed' in str(e.value)



import sqlite3

import pytest
from flaskr.db import get_db


def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        # database connection should always be the same
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')
    # database should be closed after a connection
    assert 'closed' in str(e.value)


def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        # method side effect is to report the call
        Recorder.called = True

    # mocks init_db() with fake_init_db()
    # as I don't actually want to call init_db()
    monkeypatch.setattr('flaskr.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])

    assert 'Initialized' in result.output
    assert Recorder.called

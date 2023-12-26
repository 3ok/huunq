from __future__ import annotations

from typing import Iterable

import pytest

from huunq.connection import connect
from huunq.connection import Connection
from huunq.cursor import Cursor
from huunq.exceptions import NotSupportedError


@pytest.fixture
def connection(q_server_port: int) -> Iterable[Connection]:
    connection = connect(port=q_server_port)
    yield connection
    connection.close()


def test_is_closed(connection: Connection) -> None:
    assert not connection.is_closed
    connection.close()
    assert connection.is_closed


def test_commit(connection: Connection) -> None:
    with pytest.raises(NotSupportedError):
        connection.commit()


def test_rollback(connection: Connection) -> None:
    with pytest.raises(NotSupportedError):
        connection.rollback()


def test_with(connection: Connection) -> None:
    with connection:
        assert not connection.is_closed
    assert connection.is_closed


def test_cursor(connection: Connection) -> None:
    cursor = connection.cursor()
    assert isinstance(cursor, Cursor)
    assert cursor.connection == connection

from __future__ import annotations

from typing import Iterable

import pytest

from huunq.connection import connect
from huunq.connection import Connection
from huunq.cursor import Cursor
from huunq.exceptions import ProgrammingError


@pytest.fixture
def connection(q_server_port: int) -> Iterable[Connection]:
    connection = connect(port=q_server_port)
    connection.q_connection(r"\l s.k_")
    yield connection
    connection.close()


@pytest.fixture
def cursor(connection: Connection) -> Iterable[Cursor]:
    cursor = connection.cursor()
    yield cursor
    cursor.close()


def test_fetchall_if_cursor_closed(cursor: Cursor) -> None:
    cursor.close()
    with pytest.raises(
        ProgrammingError, match=r"Cannot operate on a closed cursor\."
    ):
        cursor.fetchall()


def test_fetchall_if_connection_closed(cursor: Cursor) -> None:
    cursor.connection.close()
    with pytest.raises(
        ProgrammingError, match=r"Cannot operate on a closed connection\."
    ):
        cursor.fetchall()

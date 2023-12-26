from __future__ import annotations

from typing import Iterable

import pytest

from huunq.connection import connect
from huunq.connection import Connection
from huunq.cursor import Cursor
from huunq.exceptions import NotSupportedError
from huunq.typing import Parameters


@pytest.fixture
def connection(q_server_port: int) -> Iterable[Connection]:
    connection = connect(port=q_server_port)
    # Without this, at testing time, executing any query will raise
    # a pykx.exceptions.QError: .s.sp
    # Some discussion here:
    # https://community.kx.com/t5/PyKX/kx-q-sql-select-from-trades-command-error/m-p/14248
    connection.q_connection(r"\l s.k_")
    yield connection
    connection.close()


@pytest.fixture
def cursor(connection: Connection) -> Iterable[Cursor]:
    cursor = connection.cursor()
    yield cursor
    cursor.close()


@pytest.mark.parametrize(
    ("operation", "parameters", "has_results"),
    (
        ("SELECT * FROM dummy_table", None, True),
        ("SELECT * FROM dummy_table WHERE x > :1", [2.0], False),
        ("SELECT * FROM dummy_table WHERE x > :1", [0.5], True),
    ),
)
def test_fetchone(
    cursor: Cursor,
    operation: str,
    parameters: Parameters | None,
    has_results: bool,
) -> None:
    cursor.execute(operation, parameters)
    results = cursor.fetchone()
    if has_results:
        assert results is not None
        assert isinstance(results, tuple)
        assert len(results) == 3
        assert cursor.description == (
            ("x", None, None, None, None, None, None),
            ("x1", None, None, None, None, None, None),
            ("x2", None, None, None, None, None, None),
        )
    else:
        assert results is None


def test_fetchone_no_result_set(cursor: Cursor) -> None:
    assert cursor.fetchone() is None


@pytest.mark.parametrize(
    ("size",),
    (
        (None,),
        (5,),
    ),
)
@pytest.mark.parametrize(
    ("operation", "parameters", "has_results"),
    (
        ("SELECT * FROM dummy_table", None, True),
        ("SELECT * FROM dummy_table WHERE x > :1", [2.0], False),
        ("SELECT * FROM dummy_table WHERE x > :1", [0.5], True),
    ),
)
def test_fetchmany(
    cursor: Cursor,
    operation: str,
    parameters: Parameters | None,
    has_results: bool,
    size: int | None,
) -> None:
    cursor.execute(operation, parameters)
    results = cursor.fetchmany(size)
    if has_results:
        assert results is not None
        assert isinstance(results, list)
        assert len(results) == size if size is not None else cursor.arraysize
        assert isinstance(results[0], tuple)
        assert len(results[0]) == 3
        assert cursor.description == (
            ("x", None, None, None, None, None, None),
            ("x1", None, None, None, None, None, None),
            ("x2", None, None, None, None, None, None),
        )
    else:
        assert results == []


def test_fetchmany_no_result_set(cursor: Cursor) -> None:
    assert cursor.fetchmany() == []


@pytest.mark.parametrize(
    ("operation", "parameters", "has_results"),
    (
        ("SELECT * FROM dummy_table", None, True),
        ("SELECT * FROM dummy_table WHERE x > :1", [2.0], False),
        ("SELECT * FROM dummy_table WHERE x > :1", [0.0], True),
    ),
)
def test_fetchall(
    cursor: Cursor,
    operation: str,
    parameters: Parameters | None,
    has_results: bool,
) -> None:
    cursor.execute(operation, parameters)
    results = cursor.fetchall()
    if has_results:
        assert results is not None
        assert isinstance(results, list)
        assert len(results) == 500 == cursor.rowcount
        assert isinstance(results[0], tuple)
        assert len(results[0]) == 3
        assert cursor.description == (
            ("x", None, None, None, None, None, None),
            ("x1", None, None, None, None, None, None),
            ("x2", None, None, None, None, None, None),
        )
    else:
        assert results == []


def test_fetchall_no_result_set(cursor: Cursor) -> None:
    assert cursor.fetchall() == []


def test_description_no_result_set(cursor: Cursor) -> None:
    assert cursor.description is None


def test_rowcount_no_result_set(cursor: Cursor) -> None:
    assert cursor.rowcount == -1


def test_setinputsizes(cursor: Cursor) -> None:
    with pytest.raises(NotSupportedError):
        cursor.setinputsizes([])


def test_setoutputsize(cursor: Cursor) -> None:
    with pytest.raises(NotSupportedError):
        cursor.setoutputsize(1)


def test_executemany(cursor: Cursor) -> None:
    with pytest.raises(NotSupportedError):
        cursor.executemany("", [])

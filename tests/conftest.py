from __future__ import annotations

import os
import socket
import subprocess
import time

import pykx
import pytest
from typing_extensions import LiteralString

q_process: subprocess.Popen[bytes] | None = None
q_port = -1


def _find_free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        _, port, *_ = s.getsockname()
        assert isinstance(port, int)
        return port


def _start_q_session(port: int) -> subprocess.Popen[bytes]:
    if "QHOME" not in os.environ:  # pragma: no cover
        raise ValueError(
            "QHOME environment variable not set. "
            "Please set it to your local q installation."
        )
    return subprocess.Popen(
        [
            "rlwrap",
            "-r",
            os.path.join(os.environ["QHOME"], "l64", "q"),
            "-p",
            str(port),
        ]
    )


def _create_dummy_table(port: int, table_name: LiteralString) -> None:
    with pykx.SyncQConnection(port=port) as connection:
        connection(f"{table_name}:([]500?1f;500?`4;500?0Ng)")


def _stop_q_session(process: subprocess.Popen[bytes]) -> None:
    process.terminate()
    process.wait()


def pytest_sessionstart(session: pytest.Session) -> None:
    global q_port
    global q_process

    q_port = _find_free_port()
    q_process = _start_q_session(q_port)
    time.sleep(1)
    _create_dummy_table(q_port, "dummy_table")


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    global q_process
    if q_process is not None:  # pragma: no cover
        _stop_q_session(q_process)


@pytest.fixture(scope="session")
def q_server_port() -> int:
    global q_port
    return q_port

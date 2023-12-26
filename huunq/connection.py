from __future__ import annotations

from multiprocessing.synchronize import Lock as ProcessLock
from threading import Lock as ThreadLock
from types import TracebackType

from pykx import SyncQConnection

from huunq.cursor import Cursor
from huunq.exceptions import NotSupportedError


class Connection:
    def __init__(
        self,
        host: str | bytes = "localhost",
        port: int | None = None,
        *,
        username: str | bytes = "",
        password: str | bytes = "",
        timeout: float = 0.0,
        large_messages: bool = True,
        tls: bool = False,
        unix: bool = False,
        wait: bool = True,
        lock: ThreadLock | ProcessLock | None = None,
        no_ctx: bool = False,
    ) -> None:
        self.host = host
        self.port = port
        self.username = username
        self.q_connection = SyncQConnection(
            host=host,
            port=port,
            username=username,
            password=password,
            timeout=timeout,
            large_messages=large_messages,
            tls=tls,
            unix=unix,
            wait=wait,
            lock=lock,
            no_ctx=no_ctx,
        )

    def __enter__(self) -> Connection:
        return self

    def __exit__(
        self,
        exc_type: type[Exception],
        exc_value: Exception,
        traceback: TracebackType,
    ) -> None:
        self.close()

    def close(self) -> None:
        self.q_connection.close()

    @property
    def is_closed(self) -> bool:
        assert isinstance(self.q_connection.closed, bool)
        return self.q_connection.closed

    def commit(self) -> None:
        raise NotSupportedError("commit() is not a supported operation")

    def rollback(self) -> None:
        raise NotSupportedError("rollback() is not a supported operation")

    def cursor(self) -> Cursor:
        return Cursor(self)


def connect(
    host: str | bytes = "localhost",
    port: int | None = None,
    *,
    username: str | bytes = "",
    password: str | bytes = "",
    timeout: float = 0.0,
    large_messages: bool = True,
    tls: bool = False,
    unix: bool = False,
    wait: bool = True,
    no_ctx: bool = False,
) -> Connection:
    """
    Connects to a remote server using the specified parameters.

    Args:
        host (str | bytes, optional): The host name to which a connection
            is to be established. Defaults to "localhost".
        port (int | None, optional): The port to which a connection
            is to be established. Defaults to None.
        username (str | bytes, optional): Username for
            q connection authorization. Defaults to "".
        password (str | bytes, optional): Password for
            q connection authorization. Defaults to "".
        timeout (float, optional): Timeout for blocking socket operations
            in seconds. If set to `0`, the socket will be non-blocking.
            Defaults to 0.0.
        large_messages (bool, optional): Whether support for messages >2GB
            should be enabled. Defaults to True.
        tls (bool, optional): Whether TLS should be used. Defaults to False.
        unix (bool, optional): Whether a Unix domain socket should be used
            instead of TCP. If set to `True`, the host parameter is ignored.
            Does not work on Windows. Defaults to False.
        wait (bool, optional): Whether the q server should send a response
            to the query (which this connection will wait to receive).
            Can be overridden on a per-call basis. If True, Python will wait
            for the q server to execute the query, and respond with the
            results. If False, the q server will respond immediately to every
            query with generic null (::), then execute them at some point
            in the future. Defaults to True.
        no_ctx (bool, optional): This parameter determines whether or not
            the context interface will be disabled. disabling the context
            interface will stop extra q queries being sent but will disable
            the extra features around the context interface. Defaults to False.

    Returns:
        Connection: The connection object.
    """
    return Connection(
        host=host,
        port=port,
        username=username,
        password=password,
        timeout=timeout,
        large_messages=large_messages,
        tls=tls,
        unix=unix,
        wait=wait,
        no_ctx=no_ctx,
    )

from __future__ import annotations

import logging

from huunq.connection import connect as connect
from huunq.connection import Connection as Connection
from huunq.cursor import Cursor as Cursor
from huunq.exceptions import DatabaseError as DatabaseError
from huunq.exceptions import DataError as DataError
from huunq.exceptions import Error as Error
from huunq.exceptions import IntegrityError as IntegrityError
from huunq.exceptions import InterfaceError as InterfaceError
from huunq.exceptions import InternalError as InternalError
from huunq.exceptions import NotSupportedError as NotSupportedError
from huunq.exceptions import OperationalError as OperationalError
from huunq.exceptions import ProgrammingError as ProgrammingError
from huunq.exceptions import Warning as Warning
from huunq.globals import apilevel as apilevel
from huunq.globals import paramstyle as paramstyle
from huunq.globals import threadsafety as threadsafety

logging.getLogger(__name__).addHandler(logging.NullHandler())


__all__ = (
    "apilevel",
    "threadsafety",
    "paramstyle",
    "connect",
    "Connection",
    "Warning",
    "Error",
    "InterfaceError",
    "DatabaseError",
    "DataError",
    "OperationalError",
    "IntegrityError",
    "InternalError",
    "ProgrammingError",
    "NotSupportedError",
    "Cursor",
)

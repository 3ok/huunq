from __future__ import annotations

import functools
import sys
from typing import Callable
from typing import TYPE_CHECKING
from typing import TypeVar

if sys.version_info >= (3, 10):  # pragma: no cover
    from typing import ParamSpec
    from typing import Concatenate
else:
    from typing_extensions import ParamSpec
    from typing_extensions import Concatenate

from huunq.exceptions import ProgrammingError

if TYPE_CHECKING:
    from huunq.cursor import Cursor


P = ParamSpec("P")
R = TypeVar("R")


def error_if_closed(
    func: Callable[Concatenate[Cursor, P], R],
) -> Callable[Concatenate[Cursor, P], R]:
    @functools.wraps(func)
    def inner(cursor: Cursor, /, *args: P.args, **kwargs: P.kwargs) -> R:
        if cursor.is_closed:
            raise ProgrammingError("Cannot operate on a closed cursor.")
        if cursor.connection.is_closed:
            raise ProgrammingError("Cannot operate on a closed connection.")
        return func(cursor, *args, **kwargs)

    return inner

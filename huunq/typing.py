from __future__ import annotations

import sys
from typing import Any
from typing import Literal
from typing import Mapping
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

if sys.version_info >= (3, 10):  # pragma: no cover
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias

APILevel: TypeAlias = Literal["1.0", "2.0"]
ThreadSafety: TypeAlias = Literal[0, 1, 2, 3]
ParamStyle: TypeAlias = Literal[
    "qmark", "numeric", "named", "format", "pyformat"
]
Description: TypeAlias = Optional[
    Tuple[
        Tuple[
            str,  # name
            Optional[int],  # type_code
            Optional[int],  # display_size
            Optional[int],  # internal_size
            Optional[int],  # precision
            Optional[int],  # scale
            Optional[int],  # null_ok
        ],
        ...,
    ]
]
Parameters: TypeAlias = Union[Sequence[Any], Mapping[Union[str, int], Any]]

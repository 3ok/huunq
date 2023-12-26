from __future__ import annotations

from typing import cast
from typing import Sequence
from typing import TYPE_CHECKING

import pykx
import sqlparams

import huunq.globals
from huunq.exceptions import NotSupportedError
from huunq.typing import Description
from huunq.typing import Parameters
from huunq.utilities import error_if_closed

if TYPE_CHECKING:
    from huunq.connection import Connection


class Cursor:
    def __init__(self, connection: Connection, /) -> None:
        """Initializes a new instance of the Cursor class.

        Args:
            connection (Connection): The connection object used by the cursor.

        Attributes:
            arraysize (int): The number of rows to fetch at a time.
        """

        self.__connection = connection
        self.__is_closed = False
        self.__result_set: pykx.Table | None = None
        self.__cursor_position: int = 0
        self.__sqlparams = sqlparams.SQLParams(
            in_style=huunq.globals.paramstyle,
            out_style="numeric_dollar",
        )
        self.arraysize: int = 1

    @property
    def result_set(self) -> pykx.Table | None:
        """The result set of the last query executed."""
        return self.__result_set

    @property
    def description(self) -> Description:
        """The description of the last query executed."""
        if self.result_set is None:
            return None
        return tuple(
            (name.py(), None, None, None, None, None, None)
            for name in self.result_set.columns
        )

    @property
    def rowcount(self) -> int:
        """The number of rows affected by the last query executed."""
        if self.result_set is None:
            return -1
        else:
            return len(self.result_set)

    @property
    def connection(self) -> Connection:
        """The connection object used by the cursor."""
        return self.__connection

    @property
    def is_closed(self) -> bool:
        """Whether the cursor is closed."""
        return self.__is_closed

    def close(self) -> None:
        """Closes the cursor."""
        self.__is_closed = True
        self.__result_set = None
        self.__cursor_position = 0

    @error_if_closed
    def execute(
        self, operation: str, parameters: Parameters | None = None
    ) -> None:
        """Executes the specified SQL operation on the database connection.

        Args:
            operation (str): The SQL operation to execute.
            parameters (Parameters | None, optional): The parameters to be used
            in the SQL operation. Defaults to None.
        """
        if parameters is not None:
            operation, parameters = self.__sqlparams.format(
                operation, parameters
            )
            self.__result_set = self.connection.q_connection.sql(
                operation, *parameters
            )
        else:
            self.__result_set = self.connection.q_connection.sql(operation)
        self.__cursor_position = 0

    @error_if_closed
    def executemany(
        self,
        operation: str,
        seq_of_parameters: Sequence[Parameters] | None = None,
    ) -> None:
        """
        **Note:** This method is not supported.

        Executes the same SQL operation multiple times with different
        sets of parameters.

        Args:
            operation (str): The SQL operation to execute.
            seq_of_parameters (Sequence[Parameters] | None, optional): A
            sequence of parameter sets. Each parameter set is a tuple or
            dictionary containing the values to be substituted into the
            operation. Defaults to None.
        """
        raise NotSupportedError("executemany() is not a supported operation")

    @error_if_closed
    def fetchone(self) -> tuple[object, ...] | None:
        """
        Fetches the next row from the result set.

        Returns:
            tuple[object, ...] | None: The next row from the result set as a
            tuple of objects, or None if there are no more rows.
        """
        if self.result_set is None:
            return None
        if self.__cursor_position >= len(self.result_set):
            return None
        selection = cast(pykx.Table, self.result_set[self.__cursor_position])
        result = self.table_to_rows(selection)
        self.__cursor_position += 1
        return result[0]

    @error_if_closed
    def fetchmany(
        self, size: int | None = None
    ) -> Sequence[tuple[object, ...]]:
        """
        Fetches the next set of rows from the result set.

        Args:
            size (int, optional): The number of rows to fetch.
            If not specified, it will fetch the number of rows
            specified by `arraysize`.

        Returns:
            Sequence[tuple[object, ...]]: A sequence of tuples representing
            the fetched rows.
        """
        if self.result_set is None:
            return []
        if size is None:
            size = self.arraysize

        selection = cast(
            pykx.Table,
            self.result_set[
                self.__cursor_position : self.__cursor_position + size
            ],
        )
        result = self.table_to_rows(selection)
        self.__cursor_position += len(result)
        return result

    @error_if_closed
    def fetchall(self) -> Sequence[tuple[object, ...]]:
        """
        Fetches all remaining rows from the result set.

        Returns:
            Sequence[tuple[object, ...]]: A sequence of tuples representing
            the fetched rows.
        """
        if self.result_set is None:
            return []
        selection = cast(pykx.Table, self.result_set[self.__cursor_position :])
        result = self.table_to_rows(selection)
        self.__cursor_position += len(selection)
        return result

    def setinputsizes(self, sizes: Sequence[int]) -> None:
        """
        **Note:** This method is not supported.

        Does nothing, as parameter sizes are inferred by the database.

        Args:
            sizes (Sequence[int]): The sizes to be used for each parameter.
        """
        raise NotSupportedError("setinputsizes() is not a supported operation")

    def setoutputsize(self, size: int, column: int | None = None) -> None:
        """
        **Note:** This method is not supported.

        Does nothing, as output sizes are inferred by the database.

        Args:
            size (int): The size to be used for each output.
            column (int | None, optional): The index of the column to set the
            output size for. Defaults to None.
        """
        raise NotSupportedError("setoutputsize() is not a supported operation")

    @staticmethod
    def table_to_rows(table: pykx.Table) -> Sequence[tuple[object, ...]]:
        """Converts a pykx.Table object to a sequence of tuples.

        Args:
            table (pykx.Table): The table to convert.

        Returns:
            Sequence[tuple[object, ...]]: A sequence of tuples representing
            the table.
        """
        return [*table.pd().itertuples(index=False, name=None)]

# huunq: DBAPI2 Interface for kdb+

## Overview

`huunq` is an experimental Python package providing a DBAPI2-compliant interface for interacting with kdb+ databases.

The project was designed as a learning tool to understand [Python's DBAPI2 specification](https://peps.python.org/pep-0249/) and KX Systems new Python-first interface for the `q` language and its time-series vector database kdb+: [`pykx`](https://code.kx.com/pykx).

It's a lightweight, easy-to-use solution for Python developers looking to integrate kdb+ into their applications.

## Features

* DBAPI2 compliant interface for kdb+.
* Context management for connection objects.
* Error handling and custom exceptions.
* Type hinting for improved readability and maintainability.

## Installation

`huunq` is installable from PyPI using `pip`.
```shell
$ pip install huunq
```

## Usage
Here's a quick start quide on using `huunq` to interact with a `kdb+` database:
```python
from huunq import connect

# Establish a connection
with connect(host="localhost", port=12345) as conn:
    # Create a cursor object
    cur = conn.cursor()
    # Execute a query
    cur.execute("SELECT * FROM mytrades WHERE price > 0.5")
    # Fetch results
    results = cur.fetchall()
```
(Remember to replace `localhost` and `12345` with your kdb+ database host and port)

## Documentation

For more detailed documentation, please refer to the docstrings within the code. Each exposed function, class, and method is documented to explain its purpose and usage.

## Disclaimer

* `huunq` is an experimental project and is not recommended for production use. It's designed primarily as a learning tool.
* `huunq` is an independant effort and is not officially affiliated with KX Systems

## License

MIT

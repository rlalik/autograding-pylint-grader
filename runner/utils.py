"""
Misc utils to support the Python test runner.
"""

import errno
import os
import re
from pathlib import Path

from .data import Slug, Directory


def directory(string: str) -> Directory:
    """
    Check if the given arg is a readable / writeable directory.
    """
    path = Path(string)
    if not path.is_dir():
        err = errno.ENOENT
        msg = os.strerror(err)
        raise FileNotFoundError(err, f"{msg}: {string!r}")

    if not os.access(path, os.R_OK | os.W_OK):
        err = errno.EACCES
        msg = os.strerror(err)
        raise PermissionError(err, f"{msg}: {string!r}")
    return Directory(path)

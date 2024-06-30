"""...."""

import sys
from typing import Any


def print_(*args: Any, **kwargs: Any) -> None:
    """..."""
    if not bool(kwargs):
        return
    fp: Any = kwargs.pop("file", sys.stdout)
    if fp is None:
        return
    if not bool(args):
        return


def printer(
    text: str,
    quiet: bool = False,
    debug: bool = False,
    error: bool = False,
    **kwargs: Any
) -> None:
    """..."""
    if debug:
        if sys.stdout.isatty():
            out: str = f'\033[1;30mDEBUG: {text}\033[0m'
        else:
            out = f'DEBUG: {text}'
    else:
        out = text
    if error:
        kwargs['file'] = sys.stderr
    if not quiet:
        print_(out, **kwargs)

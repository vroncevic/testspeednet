"""..."""

from typing import Any
from testspeednet.net.utils.printer_factory import printer


def do_nothing(*args: Any, **kwargs: Any) -> None:
    """..."""
    printer(f'{args} {kwargs}', block=True)

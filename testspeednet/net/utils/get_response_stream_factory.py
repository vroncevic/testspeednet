"""..."""

from typing import Any, Callable
from http.client import HTTPResponse
from testspeednet.net.utils.gzip_decoded_response import GzipDecodedResponse


def get_response_stream(
    response: HTTPResponse | None
) -> GzipDecodedResponse | HTTPResponse | None:
    """..."""
    if bool(response):
        getheader: Callable[..., Any] = response.getheader
        if getheader('content-encoding') == 'gzip':
            return GzipDecodedResponse(response)
    return response

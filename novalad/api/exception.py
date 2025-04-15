from __future__ import annotations
from typing import TYPE_CHECKING, Any, Optional, cast
import httpx


class NovaladException(Exception):
    pass


class InvalidArgumentException(Exception):
    pass


class FileNotUploaded(Exception):
    pass

class FileFormatNotSupportedException(Exception):
    pass


class APIError(NovaladException):
    message: str

    def __init__(self, message: str) -> None:
        self.message = message

    def __repr__(self):
        return repr(self.__dict__)


class APIConnectionError(APIError):
    def __init__(self, *, message: str = "Connection error.") -> None:
        super().__init__(message) 


class APITimeoutError(APIConnectionError):
    def __init__(self) -> None:
        super().__init__(message="Request timed out.") 


class RateLimitError(APIError):
    def __init__(self) -> None:
        super().__init__(message="You have reached the rate limit.") 


class AuthenticationError(APIError):
    def __init__(self,message) -> None:
        super().__init__(message=message)


class InvalidAPIKeyError(APIError):
    def __init__(self) -> None:
        super().__init__(message="Missing/Invalid API Key.")

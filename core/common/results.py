from typing import Generic, TypeVar, Optional

from core.common.error_messages import ErrorMessage

T = TypeVar('T')


class Result(Generic[T]):
    def __init__(self, is_success: bool, error: Optional[ErrorMessage] = None, value: Optional[T] = None,
                 status_code: Optional[int] = None):
        self.is_success = is_success
        self.error = error
        self._value = value
        self.status_code = status_code

    @property
    def failure(self) -> bool:
        return not self.is_success

    @property
    def value(self) -> T:
        if not self.is_success:
            raise ValueError("Cannot Fetch value from failed result")
        return self._value

    @staticmethod
    def ok(value: Optional[T] = None, status_code: Optional[int] = None) -> 'Result[T]':
        return Result(is_success=True, value=value, status_code=status_code)

    @staticmethod
    def fail(error: ErrorMessage, status_code: Optional[int] = None) -> 'Result[T]':
        return Result(is_success=False, error=error, status_code=status_code)

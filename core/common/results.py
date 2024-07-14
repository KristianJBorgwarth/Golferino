from typing import Generic, TypeVar, Optional

from core.common.error_messages import ErrorMessage

T = TypeVar('T')


class Result(Generic[T]):
    def __init__(self, success: bool, error: Optional[ErrorMessage] = None, value: Optional[T] = None):
        self.success = success
        self.error = error
        self._value = value

    @property
    def failure(self) -> bool:
        return not self.success

    @property
    def value(self) -> T:
        if not self.success:
            raise ValueError("Cannot Fetch value from failed result")
        return self._value

    @staticmethod
    def ok(value: Optional[T] = None) -> 'Result[T]':
        return Result(success=True, value=value)

    @staticmethod
    def fail(error: ErrorMessage) -> 'Result[T]':
        return Result(success=False, error=error)

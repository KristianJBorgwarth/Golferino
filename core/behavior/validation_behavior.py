from typing import Callable
from core.common.mediator import PipeLineBehavior, R, T
from core.common.results import Result


class ValidationBehavior(PipeLineBehavior[R, T]):
    def __init__(self, serializer_class):
        self.serializer_class = serializer_class

    def handle(self, request: R, next_handler: 'Callable[[R], T]') -> T:
        serializer = self.serializer_class(data=request.__dict__)
        if not serializer.is_valid():
            return Result.fail(serializer.errors, status_code=400)
        
        return next_handler(request)

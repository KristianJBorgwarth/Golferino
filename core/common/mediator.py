from abc import ABC, abstractmethod
from typing import Optional, Any, TypeVar, Generic, Type, Dict

# Generic variable for all Requests
R = TypeVar('R', bound='Request')
T = TypeVar('T')


class Request(ABC, Generic[T]):
    """
    Base class for all command and query requests.
    Inherit from this class to define custom requests.
    """
    pass


class RequestHandler(ABC, Generic[R, T]):
    """
    Abstract base class for handling specific types of requests.
    Implement the handle method to define how the request should be processed.
    """

    @abstractmethod
    def handle(self, request: R) -> T:
        """
        Handle the given request.

        :param request: The request to handle.
        :return: result of type T from handling the request.
        """
        pass

class PipeLineBehavior(ABC, Generic[R, T]):
    
    @abstractmethod
    def handle(self, request: 'Request[T]', next_handler: 'RequestHandler[R, T]') -> T:
        """
        Handle the given request.

        :param request: The request to handle.
        :return: result of type T from handling the request.
        """
        pass

class Mediator:
    """
    Mediator class to register handlers and dispatch requests to the appropriate handler.
    """

    def __init__(self):
        """
        Initialize the Mediator with an empty dictionary for handlers.
        """
        self._handlers: Dict[Type[Request], RequestHandler] = {}

    def send(self, request: R) -> T:
        """
        Send the given request to the appropriate handler.

        :param request: The request to be handled.
        :return: Result of type T from the handler.
        :raises ValueError: If no handler is registered for the request type.
        """
        request_type = type(request)
        if request_type in self._handlers:
            handler: RequestHandler[R, T] = self._handlers[request_type]
            return handler.handle(request)
        else:
            raise ValueError(f"No handler registered for request: {request_type.__name__}")

    def register_handler(self, request_type: Type[R], handler: RequestHandler[R, T]):
        """
        Register a handler for a specific type of request.

        :param request_type: The type of request the handler will handle.
        :param handler: The handler that will process the request.
        """
        self._handlers[request_type] = handler

from abc import ABC, abstractmethod
from typing import Callable, List, Optional, Any, TypeVar, Generic, Type, Dict

# Generic variable for all Requests
T = TypeVar('T')
R = TypeVar('R', bound='Request[ABC, T]')

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

class PipelineBehavior(ABC, Generic[R, T]):
    
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
        self._handler_pipeline_factories: Dict[Type[Request], List[Callable[[None], Any]]] = {}
    
    def send(self, request: R) -> T:
        request_type = type(request)
        if request_type not in self._handler_pipeline_factories:
            raise ValueError(f"No handler registered for request: {request_type.__name__}")

        pipeline_instances = [factory() for factory in self._handler_pipeline_factories[request_type]]
        return self._execute_pipeline(pipeline_instances, 0, request)
    
    def _execute_pipeline(self, pipeline_instances: List[Any], index: int, request: R) -> T:
        if index < len(pipeline_instances):
            current_handler = pipeline_instances[index]
            if isinstance(current_handler, PipelineBehavior):
                return current_handler.handle(request, lambda r: self._execute_pipeline(pipeline_instances, index + 1, r))
            else:
                return current_handler.handle(request)
        else:
            raise ValueError("No handler found for the request type")
        
    def register_pipeline(self, request_type: Type[R], pipeline_factories: List[Callable[[], Any]]):
        self._handler_pipeline_factories[request_type] = pipeline_factories
        
    
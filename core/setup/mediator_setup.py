from core.commands.location.create.create_location_command import CreateLocationCommand
from core.commands.location.create.create_location_command_handler import CreateLocationCommandHandler
from core.common.mediator import Mediator

# Initialize a single instance of the mediator
mediator = Mediator()


# TODO: Look into handling the registration of handlers dynamically during runtime (instantiating a handler upon request) to avoid potential race conditions, if any?
def register_handlers():
    """
    Register all request handlers with the mediator.
    This function is called once at application startup.
    """
    mediator.register_handler(CreateLocationCommand, CreateLocationCommandHandler())


def get_mediator() -> Mediator:
    """
    Get the mediator instance.
    This function can be used to access the mediator elsewhere in the application.
    """
    return mediator

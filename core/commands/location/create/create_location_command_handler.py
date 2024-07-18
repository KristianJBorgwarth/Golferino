from core.commands.location.create.create_location_command import CreateLocationCommand
from core.common.results import Result
from core.data_access.repositories.location_repository import LocationRepository
from core.common.mediator import RequestHandler


class CreateLocationHandler(RequestHandler[CreateLocationCommand]):
    def __init__(self):
        self._location_repository = LocationRepository()

    def handle(self, command: CreateLocationCommand) -> Result:
        pass

import logging
from core.features.location.commands.create.create_location_command import CreateLocationCommand
from core.common.error_messages import ErrorMessage
from core.common.results import Result
from core.data_access.models.location_model import Location
from core.data_access.repositories.location_repository import LocationRepository
from core.common.mediator import RequestHandler
from core.dtos.location_dto import LocationDto


class CreateLocationCommandHandler(RequestHandler[CreateLocationCommand, Result[LocationDto]]):
    def __init__(self):
        self.location_repository = LocationRepository(Location)
        self.logger = logging.getLogger(__name__)
        
    def handle(self, command: CreateLocationCommand) -> Result[LocationDto]:
        try:
            
            location = Location(None, command.locationname, command.address, command.city)

            if self.location_repository.exists(locationname=location.locationname):
                return Result.fail(ErrorMessage.already_exists(field_name=location.locationname), status_code=400)

            location = self.location_repository.create(location)
            locationDto = LocationDto(location)

            return Result.ok(locationDto.data, status_code=200)

        except Exception as e:
            self.logger.error("An error occurred while handling the command: %s", str(e), exc_info=True)
            return Result.fail(error="An unexpected error occured", status_code=500)

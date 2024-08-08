from core.commands.location.create.create_location_command import CreateLocationCommand
from core.common.error_messages import ErrorMessage
from core.common.results import Result
from core.data_access.models.location_model import Location
from core.data_access.repositories.location_repository import LocationRepository
from core.common.mediator import RequestHandler
from core.dtos.location_dto import LocationDto


class CreateLocationCommandHandler(RequestHandler[CreateLocationCommand, Result[LocationDto]]):
    def __init__(self):
        self.location_repository = LocationRepository(Location)

    def handle(self, command: CreateLocationCommand) -> Result[LocationDto]:
        location = Location(None, command.locationname, command.address, command.city) 

        if self.location_repository.location_exists(locationname=location.locationname):
            return Result.fail(ErrorMessage.already_exists(field_name=location.locationname), status_code=400)

        location = self.location_repository.create(location)
        locationDto = LocationDto(location)

        return Result.ok(locationDto.data, status_code=200)

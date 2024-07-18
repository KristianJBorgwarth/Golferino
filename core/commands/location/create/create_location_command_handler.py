from core.commands.location.create.create_location_command import CreateLocationCommand
from core.common.error_messages import ErrorMessage
from core.common.results import Result
from core.data_access.models.location_model import Location
from core.data_access.repositories.location_repository import LocationRepository
from core.common.mediator import RequestHandler
from core.dtos.location_dto import LocationDto
from core.serializers.location.create_location_cmd_serializer import CreateLocationCommandSerializer


class CreateLocationCommandHandler(RequestHandler[CreateLocationCommand, Result[LocationDto]]):
    def __init__(self):
        self.location_repository = LocationRepository(Location)

    # TODO: write unit test for this
    def handle(self, command: CreateLocationCommand) -> Result[LocationDto]:
        serializer = CreateLocationCommandSerializer(data={
            'locationname': command.locationname,
            'address': command.address,
            'city': command.city
        })
        if not serializer.is_valid():
            return Result.fail(error=serializer.errors)

        location_data = serializer.validated_data

        if self.location_repository.location_exists(location_data['locationname']):
            return Result.fail(ErrorMessage.already_exists(location_data['locationname']))

        location = self.location_repository.create(location_data)
        locationDto = LocationDto(location)

        return Result.ok(locationDto.data)

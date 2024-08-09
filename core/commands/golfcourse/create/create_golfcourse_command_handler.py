from core.commands.golfcourse.create.create_golfcourse_command import CreateGolfcourseCommand
from core.commands.location.create.create_location_command import CreateLocationCommand
from core.common.error_messages import ErrorMessage
from core.common.results import Result
from core.data_access.models.golfcourse_model import Golfcourse
from core.data_access.models.location_model import Location
from core.data_access.repositories.golfcourse_repository import GolfcourseRepository
from core.common.mediator import RequestHandler
from core.data_access.repositories.location_repository import LocationRepository
from core.dtos.golfcourse_dto import GolfcourseDto
from core.serializers.golfcourse.create_golfcourse_cmd_serializer import CreateGolfcourseCommandSerializer


class CreateGolfcourseCommandHandler(RequestHandler[CreateGolfcourseCommand, Result[GolfcourseDto]]):
    def __init__(self):
        self.golfcourse_repository = GolfcourseRepository(Golfcourse)
        self.location_repository = LocationRepository(Location)

    def handle(self, command: CreateGolfcourseCommand) -> Result[GolfcourseDto]:
        golfcourse = Golfcourse(None, command.locationid, command.numholes, command.name
                                )
        if not self.location_repository.location_exists(locationid=command.locationid):
            return Result.fail(ErrorMessage.not_found(f"Location with id ({command.locationid}) does not exist..."),
                               status_code=400)
        if self.golfcourse_repository.golfcourse_exists(name=golfcourse.name):
            return Result.fail(ErrorMessage.already_exists(golfcourse.name), status_code=400)

        golfcourse = self.golfcourse_repository.create(golfcourse)
        golfcourseDto = GolfcourseDto(golfcourse)

        return Result.ok(golfcourseDto.data, status_code=200)
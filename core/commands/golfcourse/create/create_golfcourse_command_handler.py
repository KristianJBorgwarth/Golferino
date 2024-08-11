import logging
from core.commands.golfcourse.create.create_golfcourse_command import CreateGolfcourseCommand
from core.common.error_messages import ErrorMessage
from core.common.results import Result
from core.data_access.models.golfcourse_model import Golfcourse
from core.data_access.models.location_model import Location
from core.data_access.repositories.golfcourse_repository import GolfcourseRepository
from core.common.mediator import RequestHandler
from core.data_access.repositories.location_repository import LocationRepository
from core.dtos.golfcourse_dto import GolfcourseDto


class CreateGolfcourseCommandHandler(RequestHandler[CreateGolfcourseCommand, Result[GolfcourseDto]]):
    def __init__(self):
        self.golfcourse_repository = GolfcourseRepository(Golfcourse)
        self.location_repository = LocationRepository(Location)
        self.logger = logging.getLogger(__name__)
        
    def handle(self, command: CreateGolfcourseCommand) -> Result[GolfcourseDto]:
        try:
            
            golfcourse = Golfcourse(None, command.locationid, command.numholes, command.name
                                )
        if not self.location_repository.exists(locationid=command.locationid):
            return Result.fail(ErrorMessage.not_found(f"Location with id ({command.locationid}) does not exist..."),
                               status_code=400)
        if self.golfcourse_repository.exists(name=golfcourse.name):
            return Result.fail(ErrorMessage.already_exists(golfcourse.name), status_code=400)

            golfcourse = self.golfcourse_repository.create(golfcourse)
            golfcourseDto = GolfcourseDto(golfcourse)

            return Result.ok(golfcourseDto.data, status_code=200)
        except Exception as e:
            self.logger.error("An error occurred while handling the command: %s", str(e), exc_info=True)
            return Result.fail(error="An unexpected error occured", status_code=500)

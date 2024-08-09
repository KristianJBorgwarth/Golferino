from core.commands.golfhole.create.create_golfhole_command import CreateGolfholeCommand
from core.common.error_messages import ErrorMessage
from core.common.results import Result
from core.data_access.models.golfcourse_model import Golfcourse
from core.data_access.repositories.golfcourse_repository import GolfcourseRepository
from core.common.mediator import RequestHandler
from core.data_access.repositories.golfhole_repository import GolfholeRepository
from core.dtos.golfhole_dto import GolfholeDto
from core.data_access.models.golfhole_model import Golfhole


class CreateGolfholeCommandHandler(RequestHandler[CreateGolfholeCommand, Result[GolfholeDto]]):
    def __init__(self):
        self.golfcourse_repository = GolfcourseRepository(Golfcourse)
        self.golfhole_repository = GolfholeRepository(Golfhole)

    def handle(self, command: CreateGolfholeCommand) -> Result[GolfholeDto]:
        golfhole = Golfhole(None, command.golfcourseid, command.length, command.par, command.number)

        if not self.golfcourse_repository.golfcourse_exists(golfcourseid=golfhole.golfcourseid):
            return Result.fail(ErrorMessage.already_exists(field_name=golfhole.golfcourseid), status_code=400)

        if self.golfhole_repository.golfhole_exists(golfcourseid=golfhole.golfcourseid, number=golfhole.number):
            return Result.fail(ErrorMessage.already_exists(field_name=golfhole.number), status_code=400)


        golfhole = self.golfhole_repository.create(golfhole)
        golfholeDto = GolfholeDto(golfhole)

        return Result.ok(golfholeDto.data, status_code=200)

from datetime import datetime

from core.commands.round.create.create_round_command import CreateRoundCommand
from core.common.error_messages import ErrorMessage
from core.common.results import Result
from core.common.mediator import RequestHandler
from core.data_access.models.golfcourse_model import Golfcourse
from core.data_access.models.round_model import Round
from core.data_access.repositories.golfcourse_repository import GolfcourseRepository
from core.data_access.repositories.round_repository import RoundRepository
from core.dtos.round_dto import RoundDto
from core.serializers.round.create_round_cmd_serializer import CreateRoundCommandSerializer


class CreateRoundCommandHandler(RequestHandler[CreateRoundCommand, Result[RoundDto]]):
    def __init__(self):
        self.round_repository = RoundRepository(Round)
        self.golfcourse_repository = GolfcourseRepository(Golfcourse)

    def handle(self, command: CreateRoundCommand) -> Result[RoundDto]:
        if not self.golfcourse_repository.golfcourse_exists(golfcourseid=command.golfcourseid):
            return Result.fail(ErrorMessage.not_found(f"Golfcourse with id {command.golfcourseid} not found ..."),
                               status_code=400)

        if not command.dateplayed:
            command.dateplayed = datetime.now().strftime(format="%Y%m%d")

        serializer = CreateRoundCommandSerializer(
            data={
                'golfcourseid': command.golfcourseid,
                'dateplayed': command.dateplayed
            })

        if not serializer.is_valid():
            return Result.fail(serializer.errors, status_code=400)

        round_data = serializer.validated_data

        round_repo = self.round_repository.create(round_data)
        roundDto = RoundDto(round_repo)

        return Result.ok(roundDto.data, status_code=200)

from core.commands.playerround.create.create_playerround_command import CreatePlayerroundCommand
from core.common.error_messages import ErrorMessage
from core.common.mediator import RequestHandler
from core.common.results import Result
from core.data_access.models.playerround_model import Playerround
from core.data_access.models.round_model import Round
from core.data_access.repositories.playerround_repository import PlayerroundRepository
from core.data_access.repositories.round_repository import RoundRepository
from core.dtos.playerround_dto import PlayerroundDto
from core.serializers.playerround.create_playerround_cmd_serializer import CreatePlayerroundCommandSerializer


class CreatePlayerroundCommandHandler(RequestHandler[CreatePlayerroundCommand, Result[PlayerroundDto]]):

    def __init__(self):
        super().__init__()
        self.playerround_repository = PlayerroundRepository(Playerround)
        self.round_repository = RoundRepository(Round)

    def handle(self, command: CreatePlayerroundCommand) -> Result[PlayerroundDto]:
        serializer = CreatePlayerroundCommandSerializer(
            data={
                'playerid': command.playerid,
                'roundid': command.roundid,
                'totalscore': '',
            }
        )
        if not serializer.is_valid():
            return Result.fail(serializer.errors, status_code=400)

        if not self.round_repository.round_exists(roundid=command.roundid):
            return Result.fail(ErrorMessage.not_found(f"round with id {command.roundid} not found ..."),
                               status_code=400)

        playerround_data = serializer.validated_data

        playerround_repo = self.playerround_repository.create(playerround_data)
        playerroundDto = PlayerroundDto(playerround_repo)

        return Result.ok(playerroundDto.data, status_code=200)

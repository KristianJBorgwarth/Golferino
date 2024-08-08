from core.commands.playerround.create.create_playerround_command import CreatePlayerroundCommand
from core.common.error_messages import ErrorMessage
from core.common.mediator import RequestHandler
from core.common.results import Result
from core.data_access.models.playerround_model import Playerround
from core.data_access.models.round_model import Round
from core.data_access.repositories.playerround_repository import PlayerroundRepository
from core.data_access.repositories.round_repository import RoundRepository
from core.dtos.playerround_dto import PlayerroundDto


class CreatePlayerroundCommandHandler(RequestHandler[CreatePlayerroundCommand, Result[PlayerroundDto]]):

    def __init__(self):
        super().__init__()
        self.playerround_repository = PlayerroundRepository(Playerround)
        self.round_repository = RoundRepository(Round)

    def handle(self, command: CreatePlayerroundCommand) -> Result[PlayerroundDto]:
        if not self.round_repository.round_exists(roundid=command.roundid):
            return Result.fail(ErrorMessage.not_found(f"round with id {command.roundid} not found ..."),
                               status_code=400)

        playerround = Playerround(None, roundid_id=command.roundid, playerid_id=command.playerid)

        playerround_repo = self.playerround_repository.create(playerround)
        playerroundDto = PlayerroundDto(playerround_repo)

        return Result.ok(playerroundDto.data, status_code=200)

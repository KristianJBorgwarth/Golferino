from core.commands.player.create.create_player_command import CreatePlayerCommand
from core.common.error_messages import ErrorMessage
from core.common.results import Result
from core.data_access.models.player_model import Player
from core.common.mediator import RequestHandler
from core.data_access.repositories.player_repository import PlayerRepository
from core.dtos.player_dto import PlayerDto


class CreatePlayerCommandHandler(RequestHandler[CreatePlayerCommand, Result[PlayerDto]]):
    def __init__(self):
        self.player_repository = PlayerRepository(Player)

    def handle(self, command: CreatePlayerCommand) -> Result[PlayerDto]:
        player = Player(None, command.firstname, command.lastname, command.email)

        if self.player_repository.player_exists(email=player.email):
            return Result.fail(ErrorMessage.already_exists(str(player.email)), status_code=400)

        player = self.player_repository.create(player)
        playerDto = PlayerDto(player)

        return Result.ok(playerDto.data, status_code=200)

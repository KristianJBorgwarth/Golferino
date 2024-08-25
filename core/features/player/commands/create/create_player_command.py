from core.common.mediator import Request
from core.common.results import Result
from core.features.player.commands.create.create_player_dto import CreatePlayerDto


class CreatePlayerCommand(Request[Result[CreatePlayerDto]]):
    def __init__(self, first_name: str, last_name: str, email: str, password: str):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

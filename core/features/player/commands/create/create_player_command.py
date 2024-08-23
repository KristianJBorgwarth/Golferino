from core.common.mediator import Request
from core.common.results import Result
from core.features.player.commands.create.create_player_dto import CreatePlayerDto


class CreatePlayerCommand(Request[Result[CreatePlayerDto]]):
    def __init__(self, firstname: str, lastname: str, email: str, password: str):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password

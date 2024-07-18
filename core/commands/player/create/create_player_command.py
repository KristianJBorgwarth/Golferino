from core.common.mediator import Request
from core.common.results import Result
from core.dtos.player_dto import PlayerDto


class CreatePlayerCommand(Request[Result[PlayerDto]]):
    def __init__(self, firstname: str, lastname: str, email: str):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email

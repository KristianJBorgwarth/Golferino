from core.common.mediator import Request
from core.common.results import Result
from core.features.playerround.commands.create.create_playerround_dto import CreatePlayerroundDto


class CreatePlayerroundCommand(Request[Result[CreatePlayerroundDto]]):
    def __init__(self, playerid: int, roundid: int):
        self.playerid = playerid
        self.roundid = roundid

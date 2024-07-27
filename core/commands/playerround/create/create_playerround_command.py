from core.common.mediator import Request
from core.common.results import Result
from core.dtos.playerround_dto import PlayerroundDto


class CreatePlayerroundCommand(Request[Result[PlayerroundDto]]):
    def __init__(self, playerid: int, roundid: int):
        self.playerid = playerid
        self.roundid = roundid

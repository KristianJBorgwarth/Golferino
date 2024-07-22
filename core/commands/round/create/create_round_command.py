from core.common.mediator import Request
from core.common.results import Result
from core.dtos.round_dto import RoundDto


class CreateRoundCommand(Request[Result[RoundDto]]):
    def __init__(self, golfcourseid, dateplayed: str):
        self.golfcourseid = golfcourseid
        self.dateplayed = dateplayed

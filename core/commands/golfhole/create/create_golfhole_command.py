from core.common.mediator import Request
from core.common.results import Result
from core.dtos.golfhole_dto import GolfholeDto


class CreateGolfholeCommand(Request[Result[GolfholeDto]]):
    def __init__(self, golfcourseid: str, length: int, par: int, number: int):
        self.golfcourseid = golfcourseid
        self.length = length
        self.par = par
        self.number = number
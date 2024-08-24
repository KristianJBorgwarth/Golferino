from core.common.mediator import Request
from core.common.results import Result
from core.features.golfhole.commands.create.create_golfhole_dto import CreateGolfholeDto


class CreateGolfholeCommand(Request[Result[CreateGolfholeDto]]):
    def __init__(self, golfcourseid: int, length: int, par: int, number: int):
        self.golfcourseid = golfcourseid
        self.length = length
        self.par = par
        self.number = number
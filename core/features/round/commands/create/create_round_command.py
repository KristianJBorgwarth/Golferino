from core.common.mediator import Request
from core.common.results import Result
from core.features.round.commands.create.create_round_dto import CreateRoundDto


class CreateRoundCommand(Request[Result[CreateRoundDto]]):
    def __init__(self, golfcourseid, dateplayed: str):
        self.golfcourseid = golfcourseid
        self.dateplayed = dateplayed

from core.common.mediator import Request
from core.common.results import Result
from core.features.score.commands.create.create_score_dto import CreateScoreDto


class CreateScoreCommand(Request[Result[CreateScoreDto]]):
    def __init__(self, playerroundid: int, golfholeid: int, strokes: int):
        self.playerroundid = playerroundid
        self.golfholeid = golfholeid
        self.strokes = strokes

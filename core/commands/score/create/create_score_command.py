from core.common.mediator import Request
from core.common.results import Result
from core.dtos.score_dto import ScoreDto


class CreateScoreCommand(Request[Result[ScoreDto]]):
    def __init__(self, playerroundid: int, golfholeid: int, strokes: int):
        self.playerroundid = playerroundid
        self.golfholeid = golfholeid
        self.strokes = strokes

from core.common.mediator import Request
from core.common.results import Result
from core.features.score.commands.update.update_score_dto import UpdateScoreDto


class UpdateScoreCommand(Request[Result[UpdateScoreDto]]):
    def __init__(self, scoreid: int, strokes: int):
        self.scoreid = scoreid
        self.strokes = strokes

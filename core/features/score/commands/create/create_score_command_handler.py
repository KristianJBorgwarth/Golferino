import logging

from core.features.score.commands.create.create_score_command import CreateScoreCommand
from core.common.error_messages import ErrorMessage
from core.common.results import Result
from core.data_access.models.playerround_model import Playerround
from core.data_access.models.score_model import Score
from core.common.mediator import RequestHandler
from core.data_access.repositories.playerround_repository import PlayerroundRepository
from core.data_access.repositories.score_repository import ScoreRepository

from core.features.score.commands.create.create_score_dto import CreateScoreDto


class CreateScoreCommandHandler(RequestHandler[CreateScoreCommand, Result[CreateScoreDto]]):
    def __init__(self):
        self.playerround_repository = PlayerroundRepository(Playerround)
        self.score_repository = ScoreRepository(Score)
        self.logger = logging.getLogger(__name__)

    def handle(self, command: CreateScoreCommand) -> Result[CreateScoreDto]:
        try:
            score = Score(None, command.playerroundid, command.golfholeid, command.strokes)

            if not self.playerround_repository.playerround_exists(playerroundid=command.playerroundid):
                print(f"{command.playerroundid} not found")

                return Result.fail(ErrorMessage.not_found(message=command.playerroundid), status_code=400)

            print(score.golfholeid)
            if self.score_repository.exists(playerroundid=command.playerroundid, golfholeid=command.golfholeid):
                return Result.fail(ErrorMessage.already_exists(field_name=command.golfholeid), status_code=400)

            score = self.score_repository.create(score)
            scoreDto = CreateScoreDto(score)
        except Exception as e:
            self.logger.error("An error occured while handling the command: %s", str(e), exc_info=True)
            return Result.fail(error="An unexpected error occured", status_code=500)
        return Result.ok(scoreDto.data, status_code=200)

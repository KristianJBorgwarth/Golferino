import logging

from core.common.error_messages import ErrorMessage
from core.common.results import Result
from core.data_access.models.score_model import Score
from core.common.mediator import RequestHandler
from core.data_access.repositories.score_repository import ScoreRepository

from core.features.score.commands.update.update_score_command import UpdateScoreCommand
from core.features.score.commands.update.update_score_dto import UpdateScoreDto


class UpdateScoreCommandHandler(RequestHandler[UpdateScoreCommand, Result[UpdateScoreDto]]):
    def __init__(self):
        self.score_repository = ScoreRepository(Score)
        self.logger = logging.getLogger(__name__)

    def handle(self, command: UpdateScoreCommand) -> Result[UpdateScoreDto]:
        try:
            if not self.score_repository.exists(scoreid=command.scoreid):
                return Result.fail(ErrorMessage.not_found(message=command.scoreid), status_code=400)

            score = self.score_repository.get_by_key(scoreid=command.scoreid)

            score.strokes = command.strokes
            score = self.score_repository.update(score)
            scoreDto = UpdateScoreDto(score)

        except Exception as e:
            self.logger.error("An error occured while handling the command: %s", str(e), exc_info=True)
            return Result.fail(error="An unexpected error occured", status_code=500)

        return Result.ok(scoreDto.data, status_code=200)

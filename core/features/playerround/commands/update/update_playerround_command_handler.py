import logging

from core.common.error_messages import ErrorMessage
from core.common.mediator import RequestHandler
from core.common.results import Result
from core.data_access.models.playerround_model import Playerround
from core.data_access.models.score_model import Score
from core.data_access.repositories.playerround_repository import PlayerroundRepository
from core.data_access.repositories.score_repository import ScoreRepository
from core.features.playerround.commands.update.update_playerround_command import UpdatePlayerroundCommand
from core.features.playerround.commands.update.update_playerround_dto import UpdatePlayerroundDto


class UpdatePlayerroundCommandHandler(RequestHandler[UpdatePlayerroundCommand, Result[UpdatePlayerroundDto]]):

    def __init__(self):
        super().__init__()
        self.playerround_repository = PlayerroundRepository(Playerround)
        self.score_repository = ScoreRepository(Score)
        self.logger = logging.getLogger(__name__)
        
    def handle(self, command: UpdatePlayerroundCommand) -> Result[UpdatePlayerroundDto]:
        try:
            if not self.playerround_repository.exists(playerroundid=command.playerroundid):
                return Result.fail(ErrorMessage.not_found(f"playerround with id {command.playerroundid} not found ..."),
                               status_code=400)

            playerround_scores = self.score_repository.get_list_by_key(playerroundid=command.playerroundid)
            totalscore: int = sum([score.strokes for score in playerround_scores])

            playerround = self.playerround_repository.get_by_key(playerroundid=command.playerroundid)
            playerround.totalscore = totalscore
            playerround_repo = self.playerround_repository.update(playerround)
            playerroundDto = UpdatePlayerroundDto(playerround_repo)

            return Result.ok(playerroundDto.data, status_code=200)
        except Exception as e:
            self.logger.error("An error occurred while handling the command: %s", str(e), exc_info=True)
            return Result.fail(error="An unexpected error occured", status_code=500)

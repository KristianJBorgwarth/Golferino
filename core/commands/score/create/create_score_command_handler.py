from core.commands.golfhole.create.create_golfhole_command import CreateGolfholeCommand
from core.commands.score.create.create_score_command import CreateScoreCommand
from core.common.error_messages import ErrorMessage
from core.common.results import Result
from core.data_access.models.golfcourse_model import Golfcourse
from core.data_access.models.playerround_model import Playerround
from core.data_access.models.score_model import Score
from core.data_access.repositories.golfcourse_repository import GolfcourseRepository
from core.common.mediator import RequestHandler
from core.data_access.repositories.golfhole_repository import GolfholeRepository
from core.data_access.repositories.playerround_repository import PlayerroundRepository
from core.data_access.repositories.score_repository import ScoreRepository
from core.dtos.golfhole_dto import GolfholeDto
from core.data_access.models.golfhole_model import Golfhole
from core.dtos.score_dto import ScoreDto


class CreateScoreCommandHandler(RequestHandler[CreateScoreCommand, Result[ScoreDto]]):
    def __init__(self):
        self.playerround_repository = PlayerroundRepository(Playerround)
        self.score_repository = ScoreRepository(Score)

    def handle(self, command: CreateScoreCommand) -> Result[ScoreDto]:
        score = Score(None, command.playerroundid, command.golfholeid, command.strokes)

        if not self.playerround_repository.playerround_exists(playerroundid=command.playerroundid):
            print(f"{command.playerroundid} not found")

            return Result.fail(ErrorMessage.not_found(message=command.playerroundid), status_code=400)

        print(score.golfholeid)
        if self.score_repository.score_exists(playerroundid=command.playerroundid, golfholeid=command.golfholeid):
            return Result.fail(ErrorMessage.already_exists(field_name=command.golfholeid), status_code=400)

        score = self.score_repository.create(score)
        scoreDto = ScoreDto(score)

        return Result.ok(scoreDto.data, status_code=200)

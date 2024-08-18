import logging
from typing import List
from core.common.mediator import RequestHandler
from core.common.results import Result
from django.core.paginator import Paginator

from core.data_access.models.golfhole_model import Golfhole
from core.data_access.models.score_model import Score
from core.data_access.repositories.golfhole_repository import GolfholeRepository
from core.data_access.repositories.score_repository import ScoreRepository

from core.features.golfhole.queries.get.get_golfhole_dto import GetGolfholeDto
from core.features.golfhole.queries.get.get_golfholes_query import GetGolfholesQuery
from core.features.score.queries.get.get_score_dto import GetScoreDto
from core.features.score.queries.get.get_scores_query import GetScoresQuery


class GetScoresQueryHandler(RequestHandler[GetScoresQuery, Result[List[GetScoreDto]]]):
    def __init__(self):
        self.score_repository = ScoreRepository(Score)
        self.logger = logging.getLogger(__name__)

    def handle(self, query: GetScoresQuery) -> Result[List[GetScoreDto]]:
        try:
            scores = self.score_repository.get_list_by_key(playerroundid=query.playerroundid)

            if not scores:
                return Result.ok([], 204)

            paginator = Paginator(scores, query.page_size)
            paged_scores = paginator.get_page(query.page)
            paged_scoreDtos = GetScoreDto(paged_scores, many=True).data

            return Result.ok(paged_scoreDtos, 200)

        except Exception as e:
            self.logger.error("An error occurred while handling the query: %s", str(e), exc_info=True)
            return Result.fail(error="An unexpected error occured", status_code=500)

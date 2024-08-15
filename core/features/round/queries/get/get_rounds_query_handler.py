import logging
from typing import List

from django.core.paginator import Paginator

from core.common.mediator import RequestHandler
from core.common.results import Result
from core.data_access.models.round_model import Round
from core.data_access.repositories.round_repository import RoundRepository
from core.features.round.queries.get.get_round_dto import GetRoundDto
from core.features.round.queries.get.get_rounds_query import GetRoundsQuery


class GetRoundsQueryHandler(RequestHandler[GetRoundsQuery, Result[List[GetRoundDto]]]):
    def __init__(self):
        self.round_repository = RoundRepository(Round)
        self.logger = logging.getLogger(__name__)

    def handle(self, query: GetRoundsQuery) -> Result[List[GetRoundDto]]:
        try:

            playerrounds = self.round_repository.get_all()

            if not playerrounds:
                return Result.ok([], 204)

            paginator = Paginator(playerrounds, query.page_size)
            paged_rounds = paginator.get_page(query.page)
            paged_roundDtos = GetRoundDto(paged_rounds, many=True).data

            return Result.ok(paged_roundDtos, 200)
        except Exception as e:
            self.logger.error("An error occurred while handling the query: %s", str(e), exc_info=True)
            return Result.fail(error="An unexpected error occured", status_code=500)

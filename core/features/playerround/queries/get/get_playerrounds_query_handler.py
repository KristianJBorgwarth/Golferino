import logging
from typing import List

from django.core.paginator import Paginator

from core.common.mediator import RequestHandler
from core.common.results import Result
from core.data_access.models.playerround_model import Playerround
from core.data_access.repositories.playerround_repository import PlayerroundRepository
from core.features.playerround.queries.get.get_playerround_dto import GetPlayerroundDto
from core.features.playerround.queries.get.get_playerrounds_query import GetPlayerroundsQuery


class GetPlayerroundsQueryHandler(RequestHandler[GetPlayerroundsQuery, Result[List[GetPlayerroundDto]]]):
    def __init__(self):
        self.playerround_repository = PlayerroundRepository(Playerround)
        self.logger = logging.getLogger(__name__)

    def handle(self, query: GetPlayerroundsQuery) -> Result[List[GetPlayerroundDto]]:
        try:

            playerrounds = self.playerround_repository.get_all_by_playerid(playerid=query.playerid)

            if not playerrounds:
                return Result.ok([], 204)

            paginator = Paginator(playerrounds, query.page_size)
            paged_playerrounds = paginator.get_page(query.page)
            paged_playerroundDtos = GetPlayerroundDto(paged_playerrounds, many=True).data

            return Result.ok(paged_playerroundDtos, 200)
        except Exception as e:
            self.logger.error("An error occurred while handling the query: %s", str(e), exc_info=True)
            return Result.fail(error="An unexpected error occured", status_code=500)

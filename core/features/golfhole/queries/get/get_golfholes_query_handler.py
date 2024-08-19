import logging
from typing import List
from core.common.mediator import RequestHandler
from core.common.results import Result
from django.core.paginator import Paginator

from core.data_access.models.golfhole_model import Golfhole
from core.data_access.repositories.golfhole_repository import GolfholeRepository

from core.features.golfhole.queries.get.get_golfhole_dto import GetGolfholeDto
from core.features.golfhole.queries.get.get_golfholes_query import GetGolfholesQuery


class GetGolfholesQueryHandler(RequestHandler[GetGolfholesQuery, Result[List[GetGolfholeDto]]]):
    def __init__(self):
        self.golfhole_repository = GolfholeRepository(Golfhole)
        self.logger = logging.getLogger(__name__)

    def handle(self, query: GetGolfholesQuery) -> Result[List[GetGolfholeDto]]:
        try:
            golfholes = self.golfhole_repository.get_list_by_key(golfcourseid=query.golfcourseid)

            if not golfholes:
                return Result.ok([], 204)

            paginator = Paginator(golfholes, query.page_size)
            paged_golfholes = paginator.get_page(query.page)
            paged_golfholeDtos = GetGolfholeDto(paged_golfholes, many=True).data

            return Result.ok(paged_golfholeDtos, 200)

        except Exception as e:
            self.logger.error("An error occurred while handling the query: %s", str(e), exc_info=True)
            return Result.fail(error="An unexpected error occured", status_code=500)

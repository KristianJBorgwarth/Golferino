import logging
from typing import List

from django.contrib.auth.models import User
from django.core.paginator import Paginator

from core.common.mediator import RequestHandler
from core.common.results import Result
from core.data_access.repositories.player_repository import PlayerRepository
from core.features.player.queries.get.get_player_dto import GetPlayerDto
from core.features.player.queries.get.get_players_query import GetPlayersQuery


class GetPlayersQueryHandler(RequestHandler[GetPlayersQuery, Result[List[GetPlayerDto]]]):
    def __init__(self):
        self.player_repository = PlayerRepository(User)
        self.logger = logging.getLogger(__name__)

    def handle(self, query: GetPlayersQuery) -> Result[List[GetPlayerDto]]:
        try:
            
            players = self.player_repository.get_all()

            if not players:
                return Result.ok([], 204)

            paginator = Paginator(players, query.page_size)
            paged_players = paginator.get_page(query.page)
            paged_playerDtos = GetPlayerDto(paged_players, many=True).data

            return Result.ok(paged_playerDtos, 200)
        except Exception as e:
            self.logger.error("An error occurred while handling the query: %s", str(e), exc_info=True)
            return Result.fail(error="An unexpected error occured", status_code=500)

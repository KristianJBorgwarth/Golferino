from typing import List

from django.core.paginator import Paginator

from core.common.mediator import RequestHandler
from core.common.results import Result
from core.data_access.models.player_model import Player
from core.data_access.repositories.player_repository import PlayerRepository
from core.dtos.player_dto import PlayerDto
from core.queries.player.get.get_players_query import GetPlayersQuery
from core.serializers.player.get_players_query_serializer import GetPlayersQuerySerializer


class GetPlayersQueryHandler(RequestHandler[GetPlayersQuery, Result[List[PlayerDto]]]):
    def __init__(self):
        self.player_repository = PlayerRepository(Player)

    def handle(self, query: GetPlayersQuery) -> Result[List[PlayerDto]]:
        players = self.player_repository.get_all()

        if not players:
            return Result.ok([], 204)

        paginator = Paginator(players, query.page_size)
        paged_players = paginator.get_page(query.page)
        paged_playerDtos = PlayerDto(paged_players, many=True).data

        return Result.ok(paged_playerDtos, 200)

from typing import List

from core.common.mediator import RequestHandler
from core.common.results import Result
from core.data_access.models.player_model import Player
from core.data_access.repositories.player_repository import PlayerRepository
from core.dtos.player_dto import PlayerDto
from core.queries.player.get.get_players_query import GetPlayersQuery


class GetPlayersQueryHandler(RequestHandler[GetPlayersQuery, Result[List[PlayerDto]]]):
    def __init__(self):
        self.location_repository = PlayerRepository(Player)

    def handle(self, query: GetPlayersQuery) -> Result[List[PlayerDto]]:
        pass
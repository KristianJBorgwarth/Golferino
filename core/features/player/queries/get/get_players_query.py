from typing import List

from core.common.mediator import Request
from core.features.player.queries.get.get_player_dto import GetPlayerDto


class GetPlayersQuery(Request[List[GetPlayerDto]]):
    def __init__(self, page: int, page_size: int):
        self.page = page
        self.page_size = page_size

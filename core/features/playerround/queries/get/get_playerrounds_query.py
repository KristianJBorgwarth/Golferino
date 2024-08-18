from typing import List

from core.common.mediator import Request
from core.features.playerround.queries.get.get_playerround_dto import GetPlayerroundDto


class GetPlayerroundsQuery(Request[List[GetPlayerroundDto]]):
    def __init__(self, page: int, page_size: int, playerid: int):
        self.page = page
        self.page_size = page_size
        self.playerid = playerid

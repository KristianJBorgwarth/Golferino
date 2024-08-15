from typing import List
from core.common.mediator import Request
from core.features.round.queries.get.get_round_dto import GetRoundDto


class GetRoundsQuery(Request[List[GetRoundDto]]):
    def __init__(self, page: int, page_size: int):
        self.page = page
        self.page_size = page_size

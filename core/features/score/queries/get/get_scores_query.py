from typing import List

from core.common.mediator import Request
from core.features.score.queries.get.get_score_dto import GetScoreDto


class GetScoresQuery(Request[List[GetScoreDto]]):
    def __init__(self, page: int, page_size: int, playerroundid: int):
        self.page = page
        self.page_size = page_size
        self.playerroundid = playerroundid

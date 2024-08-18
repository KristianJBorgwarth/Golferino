from typing import List
from rest_framework import serializers

from core.common.mediator import Request
from core.dtos.player_dto import PlayerDto
from core.features.score.queries.get.get_score_dto import GetScoreDto


class GetScoresQuery(Request[List[GetScoreDto]]):
    def __init__(self, page: int, page_size: int, playerroundid: int):
        self.page = page
        self.page_size = page_size
        self.playerroundid = playerroundid

from typing import List
from rest_framework import serializers

from core.common.mediator import Request
from core.dtos.player_dto import PlayerDto


class GetPlayersQuery(Request[List[PlayerDto]]):
    def __init__(self, page: int, page_size: int):
        self.page = page
        self.page_size = page_size

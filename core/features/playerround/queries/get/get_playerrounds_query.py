from typing import List
from rest_framework import serializers

from core.common.mediator import Request
from core.dtos.player_dto import PlayerDto


class GetPlayerroundsQuery(Request[List[PlayerDto]]):
    def __init__(self, page: int, page_size: int, playerid: int):
        self.page = page
        self.page_size = page_size
        self.playerid = playerid

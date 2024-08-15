from typing import List

from core.common.mediator import Request
from core.features.golfhole.queries.get.get_golfhole_dto import GetGolfholeDto


class GetGolfholesQuery(Request[List[GetGolfholeDto]]):
    def __init__(self, page: int, page_size: int, golfcourseid: int):
        self.page = page
        self.page_size = page_size
        self.golfcourseid = golfcourseid

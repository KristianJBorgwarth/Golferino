from typing import List

from core.common.mediator import Request
from core.features.location.queries.get.get_location_dto import GetLocationDto


class GetLocationsQuery(Request[List[GetLocationDto]]):
    def __init__(self, page: int, page_size: int):
        self.page = page
        self.page_size = page_size

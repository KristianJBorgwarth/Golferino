from typing import List

from core.common.mediator import Request
from core.dtos.golfcourse_dto import GolfcourseDto


class GetGolfcoursesQuery(Request[List[GolfcourseDto]]):
    def __init__(self, page: int, page_size: int):
        self.page = page
        self.page_size = page_size

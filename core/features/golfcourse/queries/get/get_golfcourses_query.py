from typing import List

from core.common.mediator import Request
from core.features.golfcourse.queries.get.get_golfcourse_dto import GetGolfcourseDto


class GetGolfcoursesQuery(Request[List[GetGolfcourseDto]]):
    def __init__(self, page: int, page_size: int):
        self.page = page
        self.page_size = page_size

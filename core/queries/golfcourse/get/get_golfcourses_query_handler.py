import logging
from typing import List
from core.common.mediator import RequestHandler
from core.common.results import Result
from django.core.paginator import Paginator

from core.data_access.models.golfcourse_model import Golfcourse
from core.data_access.repositories.golfcourse_repository import GolfcourseRepository
from core.dtos.golfcourse_dto import GolfcourseDto
from core.queries.golfcourse.get.get_golfcourses_query import GetGolfcoursesQuery


class GetGolfcoursesQueryHandler(RequestHandler[GetGolfcoursesQuery, Result[List[GolfcourseDto]]]):
    def __init__(self):
        self.golfcourse_repository = GolfcourseRepository(Golfcourse)
        self.logger = logging.getLogger(__name__)

    def handle(self, query: GetGolfcoursesQuery) -> Result[List[GolfcourseDto]]:
        try:
            golfcourses = self.golfcourse_repository.get_all()

            if not golfcourses:
                return Result.ok([], 204)

            paginator = Paginator(golfcourses, query.page_size)
            paged_golfcourses = paginator.get_page(query.page)
            paged_golfcourseDtos = GolfcourseDto(paged_golfcourses, many=True).data

            return Result.ok(paged_golfcourseDtos, 200)

        except Exception as e:
            self.logger.error("An error occurred while handling the query: %s", str(e), exc_info=True)
            return Result.fail(error="An unexpected error occured", status_code=500)

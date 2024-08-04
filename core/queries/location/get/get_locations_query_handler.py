import logging
from typing import List
from core.common.mediator import RequestHandler
from core.common.results import Result
from django.core.paginator import Paginator
from core.data_access.models.location_model import Location
from core.data_access.repositories.location_repository import LocationRepository
from core.dtos.location_dto import LocationDto
from core.queries.location.get.get_locations_query import GetLocationsQuery


class GetLocationsQueryHandler(RequestHandler[GetLocationsQuery, Result[List[LocationDto]]]):
    def __init__(self):
        self.location_repository = LocationRepository(Location)
        self.logger = logging.getLogger(__name__)
        print("GetLocationsQueryHandler initialized")

        
    def handle(self, query: GetLocationsQuery) -> Result[List[LocationDto]]:
        try:
            locations = self.location_repository.get_all()
        
            if not locations:
                return Result.ok([], 204)
        
            paginator = Paginator(locations, query.page_size)
            paged_locations = paginator.get_page(query.page)
            paged_locationDtos = LocationDto(paged_locations, many=True).data
        
            return Result.ok(paged_locationDtos, 200)
        
        except Exception as e:
            self.logger.error("An error occurred while handling the query: %s", str(e), exc_info=True)
            return Result.fail(error="An unexpected error occured", status_code=500)
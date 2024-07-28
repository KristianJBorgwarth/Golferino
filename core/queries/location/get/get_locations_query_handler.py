
import logging
from typing import List

from core.common.mediator import RequestHandler
from core.common.results import Result
from django.core.paginator import Paginator
from core.data_access.models.location_model import Location
from core.data_access.repositories.location_repository import LocationRepository
from core.dtos.location_dto import LocationDto
from core.queries.location.get.get_locations_query import GetLocationsQuery
from core.serializers.location.get_locations_query_serializer import GetLocationsQuerySerializer

class GetLocationsQueryHandler(RequestHandler[GetLocationsQuery, Result[List[LocationDto]]]):
    def __init__(self):
        self.location_repository = LocationRepository(Location)

        
    def handle(self, query: GetLocationsQuery) -> Result[List[LocationDto]]:
        serializer = GetLocationsQuerySerializer(data={
            'page': query.page,
            'page_size': query.page_size
        })
        if not serializer.is_valid():
            return Result.fail(error=serializer.errors, status_code=400)
        locations = self.location_repository.get_all()
        logging.getLogger(__name__).info("Locations: %s", locations)
        print("FUUUUUUUUCK")
        
        if not locations:
            return Result.ok([], 204)
        
        paginator = Paginator(locations, query.page_size)
        paged_locations = paginator.get_page(query.page)
        paged_locationDtos = LocationDto(paged_locations, many=True).data
        
        return Result.ok(paged_locationDtos, 200)
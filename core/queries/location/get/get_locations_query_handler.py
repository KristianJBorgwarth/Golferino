
from typing import List
from core.common.mediator import RequestHandler
from core.common.results import Result
from core.data_access.models.location_model import Location
from core.data_access.repositories.location_repository import LocationRepository
from core.dtos.location_dto import LocationDto
from core.queries.location.get.get_locations_query import GetLocationsQuery


class GetLocationsQueryHandler(RequestHandler[GetLocationsQuery, Result[List[LocationDto]]]):
    def __init__(self):
        self.location_repository = LocationRepository(Location)
        
    def handle(self, query: GetLocationsQuery) -> Result[List[LocationDto]]:
        pass
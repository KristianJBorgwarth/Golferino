from core.common.mediator import Request
from core.common.results import Result
from core.dtos.location_dto import LocationDto


class CreateLocationCommand(Request[Result[LocationDto]]):
    def __init__(self, locationname: str, address: str, city: str):
        self.locationname = locationname
        self.address = address
        self.city = city

from core.common.mediator import Request
from core.common.results import Result
from core.features.location.commands.create.create_location_dto import CreateLocationDto


class CreateLocationCommand(Request[Result[CreateLocationDto]]):
    def __init__(self, locationname: str, address: str, city: str):
        self.locationname = locationname
        self.address = address
        self.city = city

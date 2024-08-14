from core.common.mediator import Request
from core.common.results import Result
from core.dtos.golfcourse_dto import GolfcourseDto


class CreateGolfcourseCommand(Request[Result[GolfcourseDto]]):
    def __init__(self, locationid: int, numholes: int, name: str):
        self.locationid = locationid
        self.numholes = numholes
        self.name = name

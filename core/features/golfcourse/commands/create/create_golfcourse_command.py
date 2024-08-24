from core.common.mediator import Request
from core.common.results import Result
from core.features.golfcourse.commands.create.create_golfcourse_dto import CreateGolfcourseDto


class CreateGolfcourseCommand(Request[Result[CreateGolfcourseDto]]):
    def __init__(self, locationid: int, numholes: int, name: str):
        self.locationid = locationid
        self.numholes = numholes
        self.name = name

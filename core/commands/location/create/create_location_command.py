from core.common.mediator import Request


class CreateLocationCommand(Request):
    def __init__(self, locationname: str, address: str, city: str):
        self.locationname = locationname
        self.address = address
        self.city = city
from core.common.mediator import Request
from core.common.results import Result
from core.features.playerround.commands.update.update_playerround_dto import UpdatePlayerroundDto


class UpdatePlayerroundCommand(Request[Result[UpdatePlayerroundDto]]):
    def __init__(self, playerroundid: int):
        self.playerroundid = playerroundid

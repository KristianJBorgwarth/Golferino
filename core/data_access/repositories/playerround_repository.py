from typing import List

from core.data_access.base_repositories.base_repository import T
from core.data_access.base_repositories.repository import Repository
from core.data_access.models.playerround_model import Playerround


class PlayerroundRepository(Repository[Playerround]):
    def init(self):
        super().__init__(Playerround)

    @staticmethod
    def playerround_exists(**kwargs) -> bool:
        return Playerround.objects.filter(**kwargs).exists()

    def get_all_by_playerid(self, playerid: int) -> List[T]:
        return list(self._model.objects.all().filter(playerid=playerid))
    
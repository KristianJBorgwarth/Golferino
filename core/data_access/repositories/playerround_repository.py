from core.data_access.base_repositories.repository import Repository
from core.data_access.models.playerround_model import Playerround


class PlayerroundRepository(Repository[Playerround]):
    def init(self):
        super().__init__(Playerround)

    @staticmethod
    def playerround_exists(**kwargs) -> bool:
        return Playerround.objects.filter(**kwargs).exists()
from core.data_access.base_repositories.repository import Repository
from core.data_access.models.golfhole_model import Golfhole


class GolfholeRepository(Repository[Golfhole]):
    def init(self):
        super().__init__(Golfhole)

    @staticmethod
    def golfhole_exists(**kwargs) -> bool:
        return Golfhole.objects.filter(**kwargs).exists()

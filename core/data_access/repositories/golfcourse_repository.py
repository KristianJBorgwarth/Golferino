from core.data_access.base_repositories.repository import Repository
from core.data_access.models.golfcourse_model import Golfcourse


class GolfcourseRepository(Repository[Golfcourse]):
    def init(self):
        super().__init__(Golfcourse)

    @staticmethod
    def golfcourse_exists(**kwargs) -> bool:
        return Golfcourse.objects.filter(**kwargs).exists()

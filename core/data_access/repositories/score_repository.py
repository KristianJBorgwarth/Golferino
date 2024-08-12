from core.data_access.base_repositories.repository import Repository
from core.data_access.models.score_model import Score


class ScoreRepository(Repository[Score]):
    def init(self):
        super().__init__(Score)

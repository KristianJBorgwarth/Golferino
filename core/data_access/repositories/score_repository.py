from typing import List

from core.data_access.base_repositories.base_repository import T
from core.data_access.base_repositories.repository import Repository
from core.data_access.models.score_model import Score


class ScoreRepository(Repository[Score]):
    def init(self):
        super().__init__(Score)

    def get_list_by_key(self, **kwargs) -> List[T]:
        return list(self._model.objects.all().filter(**kwargs))

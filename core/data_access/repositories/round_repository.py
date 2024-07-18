from core.data_access.base_repositories.repository import Repository
from core.data_access.models.round_model import Round


class RoundRepository(Repository[Round]):
    def init(self):
        super().__init__(Round)

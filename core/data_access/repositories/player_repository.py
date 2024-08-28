from django.contrib.auth.models import User

from core.data_access.base_repositories.repository import Repository


class PlayerRepository(Repository[User]):
    def init(self):
        super().__init__(User)

from typing import Optional

from core.common.results import T
from core.data_access.base_repositories.repository import Repository
from core.data_access.models.player_model import Player


class PlayerRepository(Repository[Player]):
    def init(self):
        super().__init__(Player)

    @staticmethod
    def email_exists(email: str) -> bool:
        return Player.objects.filter(email=email).exists()

    @staticmethod
    def player_exists(**kwargs) -> bool:
        return Player.objects.filter(**kwargs).exists()

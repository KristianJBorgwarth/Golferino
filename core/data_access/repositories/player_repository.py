from core.data_access.base_repositories.repository import Repository
from core.data_access.models.player.player_model import Player


class PlayerRepository(Repository[Player]):
    def init(self):
        super().__init__(Player)
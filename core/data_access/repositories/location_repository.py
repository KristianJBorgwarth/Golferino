from core.data_access.base_repositories.repository import Repository
from core.data_access.models.location_model import Location


class LocationRepository(Repository[Location]):
    def init(self):
        super().__init__(Location)

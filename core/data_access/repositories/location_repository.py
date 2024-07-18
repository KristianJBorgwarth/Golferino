from core.data_access.base_repositories.repository import Repository
from core.data_access.models.location_model import Location


class LocationRepository(Repository[Location]):
    def init(self):
        super().__init__(Location)

    @staticmethod
    def location_exists(location_name: str) -> bool:
        return Location.objects.filter(locationname=location_name).exists()

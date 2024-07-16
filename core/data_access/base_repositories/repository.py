from typing import Type, List, Optional, Dict, Any
from django.db import transaction
from django.db.models import Model
from .base_repository import BaseRepository, T


class Repository(BaseRepository[T]):
    def __init__(self, model: Type[Model]):
        self._model = model

    def get_all(self) -> List[T]:
        return list(self._model.objects.all())

    def get_by_key(self, **kwargs) -> Optional[T]:
        try:
            return self._model.objects.get(**kwargs)
        except self._model.DoesNotExist:
            return None

    def create(self, obj: Dict[str, Any]) -> T:
        instance = self._model(**obj)
        instance.save()
        return instance

    def update(self, obj: T) -> T:
        obj.save()
        return obj

    def delete(self, id: int) -> None:
        self._model.objects.filter(pk=id).delete()

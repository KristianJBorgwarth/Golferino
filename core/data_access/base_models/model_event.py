from core.common.mediator import Notification
from django.utils import timezone

class ModelEvent(Notification):
    """Base class for all model events."""
    def __init__(self):
        self._triggered_at = timezone.now()
    
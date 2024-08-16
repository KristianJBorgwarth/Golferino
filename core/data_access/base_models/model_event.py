from datetime import timezone
from core.common.mediator import Notification


class ModelEvent(Notification):
    """Base class for all model events."""
    def __init__(self):
        self._triggered_at = timezone.now()
    
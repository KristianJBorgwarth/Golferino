from django.utils import timezone
from django.db import models
from core.data_access.base_models.model_event import ModelEvent


class BaseModel(models.Model):
    _events = []
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   
    class Meta:
        abstract = True
        
    def add_event(self, event: ModelEvent):
        """Add an event to the list of events."""
        self._events.append(event)
        
    def _clear_events(self):
        """Clear the list of events."""
        self._events = []

    def dispatch_events(self):
        """Dispatch all events."""
        if self._events.count == 0: 
            return
        for event in self._events:
            from core.setup.mediator_setup import get_mediator  # Local import to avoid circular dependencies
            get_mediator().publish(event)
        self._clear_events()
        
    def save(self, *args, **kwargs):
        """Override the save method to dispatch events and update timestamps."""
        if not self.created_at:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
        self.dispatch_events()

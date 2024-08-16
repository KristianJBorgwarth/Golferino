import logging
from core.common.mediator import NotificationHandler
from core.data_access.models.player.player_created_event import PlayerCreatedEvent
from core.services.email.email_service import EmailSerivce


class PlayerCreatedEventHandler(NotificationHandler):
    def __init__(self):
        self.email_service = EmailSerivce()
        self.logger = logging.getLogger(__name__)

    def handle(self, event: PlayerCreatedEvent):
        try:
            print("cant believe this is working")
            
        except Exception as e:
            self.logger.error("An error occurred while handling the event: %s", str(e), exc_info=True)
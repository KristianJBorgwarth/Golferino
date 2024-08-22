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
            
            self.email_service.send(to_email=event.player.email, 
                                    subject="Welcome to Golferino", 
                                    message=f"Hi {event.player.firstname}, welcome to Golferino! Here is your verification code: {event.verification_code.code}")
            
        except Exception as e:
            self.logger.error("An error occurred while handling the event: %s", str(e), exc_info=True)
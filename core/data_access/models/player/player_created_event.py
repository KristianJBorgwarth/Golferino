from django.contrib.auth.models import User

from core.data_access.base_models.model_event import ModelEvent
from core.data_access.models.verification_code_model import VerificationCode


class PlayerCreatedEvent(ModelEvent):
    def __init__(self, code: VerificationCode, player: User):
        self.verification_code = code
        self.player = player
        super().__init__()
from datetime import datetime, timedelta
from core.common.results import Result
from core.data_access.models.player.player_model import Player
from core.data_access.models.verification_code_model import VerificationCode
import random

class VerificationCodeService:
    def generate_verification_code(self, player: Player) -> VerificationCode:
        code = random.randint(0, 999999)
        formatted_code = str(code).zfill(6)
        verification_code = VerificationCode(code=formatted_code, is_used=False, player=player, expiration_date=datetime.now() + timedelta(minutes=5))
        return verification_code
    
    def validate_verification_codes(self, code_to_validate: str, code: VerificationCode) -> Result:
        if code.is_used:
            return Result.fail("Verification code is already used", status_code=400)
        
        if code.expiration_date < datetime.now():
            return Result.fail("Verification code is expired", status_code=400)
        
        if code_to_validate != code.code:
            return Result.fail("Verification code is invalid", status_code=400)
        
        return Result.ok()
    
    def mark_verification_code_as_used(self, verification_code: VerificationCode) -> VerificationCode:
        verification_code.is_used = True
        return verification_code
    
    
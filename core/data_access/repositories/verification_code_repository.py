from core.data_access.base_repositories.repository import Repository
from core.data_access.models.verification_code_model import VerificationCode


class VerificationCodeRepository(Repository[VerificationCode]):
    def init(self):
        super().__init__(VerificationCode)

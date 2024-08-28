from django.http import JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from core.data_access.models.verification_code_model import VerificationCode


class VerifyEmailView(View):
    @swagger_auto_schema(
        request_body=int,
        responses={200: 'Email successfully verified!', 404: 'Verification code not found'}
    )
    def get(self, code):
        verification_code = get_object_or_404(VerificationCode, code=code, is_used=False)
        verification_code.is_used = True
        verification_code.user.is_verified = True
        verification_code.user.save()
        verification_code.save()

        return JsonResponse({"message": "Email successfully verified!"})

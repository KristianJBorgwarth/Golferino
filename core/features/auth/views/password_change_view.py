from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from core.common.ResponseEnvelope import ResponseEnvelope
from core.features.auth.serializers.password_change_serializer import PasswordChangeSerializer


class PasswordChangeView(viewsets.ViewSet):
    @swagger_auto_schema(
        request_body=PasswordChangeSerializer,
        responses={200: 'OK', 400: 'BadRequest'}
    )
    def update(self, request):
        if not request.user.is_authenticated:
            return ResponseEnvelope.fail('Authentication required', 401)

        serializer = PasswordChangeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Password has been changed."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

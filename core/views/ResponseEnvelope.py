# core/common/response_envelope.py

from rest_framework.response import Response
from rest_framework import status


class ResponseEnvelope:
    def __init__(self, success, data=None, error=None, status_code=status.HTTP_200_OK):
        self.success = success
        self.data = data
        self.error = error
        self.status_code = status_code

    @staticmethod
    def success(data=None, message=None, status_code=status.HTTP_200_OK):
        return ResponseEnvelope(success=True, data=data, status_code=status_code)

    @staticmethod
    def fail(error, message=None, status_code=status.HTTP_400_BAD_REQUEST):
        return ResponseEnvelope(success=False, error=error, status_code=status_code)

    def to_response(self):
        response_data = {
            'success': self.success,
            'data': self.data,
            'error': self.error,
        }
        return Response(response_data, status=self.status_code)

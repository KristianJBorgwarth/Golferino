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
    def success(data, status_code):
        return Response({
            'success': True,
            'data': data,
            'error': None
        }, status=status_code)

    @staticmethod
    def fail(error, status_code):
        return Response({
            'success': False,
            'data': None,
            'error': error
        }, status=status_code)


    #TODO: remove this method, it is not used
    @staticmethod
    def to_response(self):
        response_data = {
            'success': self.success,
            'data': self.data,
            'error': self.error,
        }
        return Response(response_data, status=self.status_code)

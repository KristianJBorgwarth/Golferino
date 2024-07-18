from rest_framework import viewsets
from rest_framework.viewsets import ViewSet


class LocationView(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
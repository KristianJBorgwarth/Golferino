from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from core.commands.score.create.create_score_command import CreateScoreCommand
from core.dtos.score_dto import ScoreDto
from core.serializers.score.create_score_cmd_serializer import CreateScoreCommandSerializer
from core.setup.mediator_setup import get_mediator
from core.views.ResponseEnvelope import ResponseEnvelope


class ScoreView(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._mediator = get_mediator()

    @swagger_auto_schema(
        request_body=CreateScoreCommandSerializer,
        responses={200: ScoreDto, 400: 'BadRequest'}
    )
    def create(self, request):
        cmd = CreateScoreCommand(request.data.get('playerroundid'),
                                 request.data.get('golfholeid'),
                                 request.data.get('strokes')
                                 )
        result = self._mediator.send(cmd)
        if result.is_success:
            return ResponseEnvelope.success(result.value, result.status_code)
        else:
            return ResponseEnvelope.fail(result.error, result.status_code)

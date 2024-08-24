from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from core.features.score.commands.create.create_score_command import CreateScoreCommand
from core.features.score.commands.create.create_score_dto import CreateScoreDto
from core.features.score.commands.create.create_score_cmd_serializer import CreateScoreCommandSerializer
from core.features.score.queries.get.get_score_dto import GetScoreDto
from core.features.score.queries.get.get_scores_query import GetScoresQuery
from core.features.score.queries.get.get_scores_query_serializer import GetScoresQuerySerializer
from core.setup.mediator_setup import get_mediator
from core.common.ResponseEnvelope import ResponseEnvelope


class ScoreView(viewsets.ViewSet):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._mediator = get_mediator()

    @swagger_auto_schema(
        request_body=CreateScoreCommandSerializer,
        responses={200: CreateScoreDto, 400: 'BadRequest'}
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

    @swagger_auto_schema(
        query_serializer=GetScoresQuerySerializer,
        responses={200: GetScoreDto(many=True), 204: 'No Content', 400: 'BadRequest'}
    )
    def get_all(self, request):
        query = GetScoresQuery(page=int(request.query_params.get('page', 1)),
                               page_size=int(request.query_params.get('page_size', 10)),
                               playerroundid=int(request.query_params.get('playerroundid')))

        result = self._mediator.send(query)
        if result.is_success:
            return ResponseEnvelope.success(result.value, result.status_code)
        else:
            return ResponseEnvelope.fail(result.error, result.status_code)
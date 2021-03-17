from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from survey import serializers
from survey.models import Survey, User, UserSurvey
from survey.services import get_survey, get_user_from_request


class SurveyView(GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.RetrieveModelMixin):
    queryset = Survey.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.SurveyListSerializer
        elif self.action == 'retrieve':
            return serializers.SurveyDetailSerializer
        elif self.action == 'save_user_answer':
            return serializers.UserSurveySerializer

    @action(methods=['post'], detail=True)
    def save_user_answer(self, request, pk):
        user = get_user_from_request(request)
        survey = get_survey(pk)
        user_survey, is_created = UserSurvey.objects.get_or_create(
            user=user,
            survey=survey
        )
        if not is_created:
            raise ValidationError(
                'The user has already completed this survey',
                code=400
            )
        serializer = self.get_serializer(user_survey, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)


class UserAuth(GenericViewSet,
               mixins.CreateModelMixin):
    queryset = User.objects.all()
    serializer_class = serializers.UserAuthSerializer


# class UserSurveyView(GenericViewSet):
#     queryset = User.objects.all()
#
#     @action(methods=['get'], detail=True)
#     def get_all_surveys(self, request, pk):
#





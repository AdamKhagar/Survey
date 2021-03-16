from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from survey import serializers
from survey.models import Survey


class SurveyView(GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.RetrieveModelMixin):
    queryset = Survey.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.SurveyListSerializer
        elif self.action == 'retrieve':
            return serializers.SurveyDetailSerializer


# class UserAuth(GenericViewSet):
#     @action
#     def registation(self):
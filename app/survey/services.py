from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError

from survey.models import Survey, User, UserSurvey


def get_survey(pk: int) -> Survey:
    try:
        return Survey.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise ValidationError('survey does not exist', 404)


def get_survey_from_request(request) -> Survey:
    try:
        return get_survey(request.data['survey'])
    except ObjectDoesNotExist:
        raise ValidationError('survey does not exist', 404)


def get_user(pk: int) -> User:
    try:
        return User.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise ValidationError('user does not exist', 404)


def get_user_from_request(request) -> User:
    return get_user(request.data['user'])


def get_user_survey(user, survey):
    try:
        return UserSurvey.objects.get(user=user, survey=survey)
    except ObjectDoesNotExist as e:
        raise ValidationError(e.args, 404)

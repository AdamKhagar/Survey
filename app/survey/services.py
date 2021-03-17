from rest_framework.exceptions import ValidationError

from survey.models import Survey, User


def get_survey(pk: int) -> Survey:
    return Survey.objects.get(pk=pk)

def get_user_from_request(request) -> User:
    try:
        user = User.objects.get(pk=request.data['user'])
    except User.DoesNotExist:
        raise ValidationError(detail='user does not exist', code=400)
    else:
        return user
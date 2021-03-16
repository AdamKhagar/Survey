from django.urls import path
from rest_framework.routers import SimpleRouter

from survey import views

router = SimpleRouter(trailing_slash=False)

router.register('surveys', views.SurveyView, basename='surveys')

urlpatterns = router.urls

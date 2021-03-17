from rest_framework.routers import SimpleRouter

from survey import views

router = SimpleRouter(trailing_slash=False)

router.register('surveys', views.SurveyView, basename='surveys')
router.register(r'user', views.UserDetailView, basename='user')

urlpatterns = router.urls

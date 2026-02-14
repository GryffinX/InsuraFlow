from rest_framework.routers import DefaultRouter
from .views import InsurerViewSet, AgentViewSet, SurveyorViewSet, ServiceProviderViewSet, PolicyViewSet

router = DefaultRouter()

router.register(r'insurers', InsurerViewSet)
router.register(r'agents', AgentViewSet)
router.register(r'surveyors', SurveyorViewSet)
router.register(r'providers', ServiceProviderViewSet)
router.register(r'policies', PolicyViewSet, basename='policy')

urlpatterns = router.urls
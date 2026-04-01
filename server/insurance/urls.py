from rest_framework.routers import DefaultRouter
from .views import (
    ProviderViewSet, AgentViewSet, SurveyorViewSet, 
    ServiceProviderViewSet, PolicyViewSet,
    UserPolicyViewSet
)

router = DefaultRouter()

router.register(r'providers', ProviderViewSet, basename='provider')
router.register(r'agents', AgentViewSet, basename='agent')
router.register(r'surveyors', SurveyorViewSet, basename='surveyor')
router.register(r'service-providers', ServiceProviderViewSet, basename='service-provider')
router.register(r'policies', PolicyViewSet, basename='policy')
router.register(r'user-policies', UserPolicyViewSet, basename='user-policy')

urlpatterns = router.urls

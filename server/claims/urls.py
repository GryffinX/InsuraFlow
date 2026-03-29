from rest_framework.routers import DefaultRouter
from .views import ClaimViewSet, InspectionReportViewSet, SettlementViewSet

router = DefaultRouter()
router.register(r'claims', ClaimViewSet, basename='claim')
router.register(r'reports', InspectionReportViewSet, basename='report')
router.register(r'settlements', SettlementViewSet, basename='settlement')

urlpatterns = router.urls
from rest_framework.routers import DefaultRouter
from .views import ClaimViewSet, InspectionReportViewSet, SettlementViewSet

router = DefaultRouter()
router.register(r'claims', ClaimViewSet)
router.register(r'reports', InspectionReportViewSet)
router.register(r'settlements', SettlementViewSet)

urlpatterns = router.urls
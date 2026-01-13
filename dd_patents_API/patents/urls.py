from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PTMainViewSet, PTPriorityClaimViewSet, PTInterestedPartyViewSet, PTAbstractViewSet, PTDisclosureViewSet, PTClaimViewSet, PTIPCClassificationViewSet
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views_detail import PTMainDetailViewSet
# Router for API endpoints
router = DefaultRouter()
router.register(r'pt_main', PTMainViewSet, basename='main')
router.register(r'pt_priority_claim', PTPriorityClaimViewSet, basename='priority_claim')
router.register(r'pt_interested_party', PTInterestedPartyViewSet, basename='interested_party')
router.register(r'pt_abstract', PTAbstractViewSet, basename='abstract')
router.register(r'pt_disclosure', PTDisclosureViewSet, basename='disclosure')
router.register(r'pt_claim', PTClaimViewSet, basename='claim')
router.register(r'pt_ipc_classification', PTIPCClassificationViewSet, basename='ipc_classification')
router.register(r'pt_main_detail', PTMainDetailViewSet, basename='main_detail')


# Swagger schema view
schema_view = get_schema_view(
    openapi.Info(
        title="Patent API",
        default_version='v1',
        description="API for managing patent data",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', include(router.urls)),
]

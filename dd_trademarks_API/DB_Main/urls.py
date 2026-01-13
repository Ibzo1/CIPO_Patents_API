from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API documentation for the Django project",
    ),
    public=True,
    authentication_classes=[], 
    permission_classes=(permissions.AllowAny,),
)


class APIRoot(APIView):
    def get(self, request):
        base = request.build_absolute_uri()
        return Response({
            "trademarks": f"{base}trademarks/",
        })

from django.http import JsonResponse

def health(request):
    return JsonResponse({"status": "ok"})

urlpatterns = [
    path('health/', health, name='health_check'),
    path('admin/', admin.site.urls),
    path("api/", APIRoot.as_view(), name="api-root"),
    path("trademarks/", include("trademarks.urls")),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # Export endpoints:
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger.yaml', schema_view.without_ui(cache_timeout=0), name='schema-yaml'),
]


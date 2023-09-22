from email.mime import base
from django.urls import include, path, re_path
from rest_framework.permissions import AllowAny
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from main.views import CustomAuthToken, CheckSessionExist


schema_view = get_schema_view(
    openapi.Info(
        title="ARS API",
        default_version="v1",
        description="RESTFUL API for Accounting Reporting System",
    ),
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    # path('auth/login/', CustomAuthToken.as_view()),
    path('auth/check/', CheckSessionExist),
    path("auth/", include("dj_rest_auth.urls")),
    path("libraries/", include("libraries.urls")),
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    re_path(
        r"^redoc/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"
    ),
]

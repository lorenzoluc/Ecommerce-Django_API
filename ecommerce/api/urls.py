from django.urls import path, include
from . import views
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="E-Shop API",
        default_version='v1',
        description="API for products management",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="lucas@loja.local"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
)

urlpatterns = [
    path('api/products/', views.getData),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]


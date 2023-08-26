from django.urls import include, path
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from rest_framework.routers import DefaultRouter

from .views import AuthView, ProfileViewSet, SignUpView

router_v1 = DefaultRouter()

router_v1.register(r'profiles', ProfileViewSet, basename='profiles')

urlpatterns = [
    path('', SpectacularAPIView.as_view(), name='schema'),
    path(
        'docs/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui'
    ),
    path(
        'redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc'
    ),
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', SignUpView.as_view(), name='signup'),
    path('v1/auth/login/', AuthView.as_view(), name='login'),
]

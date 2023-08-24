from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import AuthView, SignUpView, UserViewSet

router_v1 = DefaultRouter()

router_v1.register(r'profiles', UserViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/signup/', SignUpView.as_view(), name='signup'),
    path('v1/login/', AuthView.as_view(), name='login'),
]

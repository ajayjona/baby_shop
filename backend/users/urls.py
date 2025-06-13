from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, VendorProfileViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'vendor-profiles', VendorProfileViewSet, basename='vendor-profile')

urlpatterns = [
    path('', include(router.urls)),
]
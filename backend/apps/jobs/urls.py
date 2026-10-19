from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobPostingViewSet

router = DefaultRouter()
router.register(r'', JobPostingViewSet, basename='job')

urlpatterns = [
    path('', include(router.urls)),
]


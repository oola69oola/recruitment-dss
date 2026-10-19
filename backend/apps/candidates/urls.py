from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CandidateSubmissionViewSet

router = DefaultRouter()
router.register(r'', CandidateSubmissionViewSet, basename='candidate')

urlpatterns = [
    path('', include(router.urls)),
]


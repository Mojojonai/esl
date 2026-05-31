"""
URL configuration for eslapp project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from accounts.views import UserViewSet, UserProfileViewSet
from learning.views import (
    LevelViewSet, UnitViewSet, LessonViewSet, 
    ExerciseViewSet, VocabularyViewSet, DialogueViewSet
)
from games.views import GameTemplateViewSet
from tracking.views import UserProgressViewSet, UserBadgeViewSet, ReviewItemViewSet

# Create routers
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'profiles', UserProfileViewSet, basename='profile')
router.register(r'levels', LevelViewSet, basename='level')
router.register(r'units', UnitViewSet, basename='unit')
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'exercises', ExerciseViewSet, basename='exercise')
router.register(r'vocabulary', VocabularyViewSet, basename='vocabulary')
router.register(r'dialogues', DialogueViewSet, basename='dialogue')
router.register(r'games', GameTemplateViewSet, basename='game')
router.register(r'progress', UserProgressViewSet, basename='progress')
router.register(r'badges', UserBadgeViewSet, basename='badge')
router.register(r'review', ReviewItemViewSet, basename='review')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/auth/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

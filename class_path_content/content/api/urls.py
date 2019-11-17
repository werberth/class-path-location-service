from django.urls import path, include

from rest_framework import routers

from . import viewsets, views

router = routers.SimpleRouter()
router.register(r'content', viewsets.ContentViewSet)
router.register(r'activity', viewsets.ActivityViewSet)
router.register(r'activity-answer', viewsets.ActivityAnswerViewSet)


urlpatterns = [
    path('', include(router.urls)),
]

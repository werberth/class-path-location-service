from django.urls import path, include

from rest_framework import routers

from . import viewsets, views

router = routers.SimpleRouter()
router.register(r'contents', viewsets.ContentViewSet, basename="Content")
router.register(r'activities', viewsets.ActivityViewSet, basename="Activity")
router.register(r'activity-answers', viewsets.ActivityAnswerViewSet, basename="ActivityAnswer")


urlpatterns = [
    path('', include(router.urls)),
]

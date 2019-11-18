from django.urls import path, include

from rest_framework import routers

from . import viewsets

router = routers.SimpleRouter()
router.register(r'location', viewsets.LocationViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('distance/', viewsets.DistanceView.as_view())
]
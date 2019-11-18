from rest_framework import viewsets, generics
from rest_framework.response import Response

from haversine import haversine, Unit

from ..models import Location

from . import serializers


class LocationViewset(viewsets.ModelViewSet):
    serializer_class = serializers.LocationSerializer
    queryset = Location.objects.all()


class DistanceView(generics.CreateAPIView):
    serializer_class = serializers.DistanceSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        origin = serializer.data['origin']
        destination = serializer.data['destination']

        distance = haversine(origin, destination, unit=Unit.METERS)

        data = {
            'threshold': serializer.data['threshold'] > distance,
            'distance': distance
        }

        return Response(data)

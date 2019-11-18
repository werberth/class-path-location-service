from rest_framework import serializers

from ..models import Location


class DistanceSerializer(serializers.Serializer):
    origin = serializers.ListField(child=serializers.FloatField(), required=True)
    destination = serializers.ListField(child=serializers.FloatField(), required=True)
    threshold = serializers.IntegerField(required=True)

    class Meta:
        fields = ('origin', 'destination', 'threshold')


class LocationSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    # teacher_id = serializers.IntegerField(required=True)
    description = serializers.CharField(required=False)

    class Meta:
        model = Location
        fields = (
            'name', 'latitude', 'longitude',
            'description', 'teacher'
        )

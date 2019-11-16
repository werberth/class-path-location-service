from rest_framework import serializers, viewsets

from ..models import Content, Activity, ActivityAnswer

from . import serializers


class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = serializers.ContentSerializer


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = serializers.ActivitySerializer


class ActivityAnswerViewSet(viewsets.ModelViewSet):
    queryset = ActivityAnswer.objects.all()
    serializer_class = serializers.ActivityAnswerSerializer

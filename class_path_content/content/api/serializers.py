from rest_framework import serializers

from ..models import Content, Activity, ActivityAnswer


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = (
            'id', 'title', 'description', 'teacher',
            'course', 'create_at', 'update_at'
        )


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = (
            'id', 'title', 'description', 'location',
            'content', 'create_at', 'update_at'
        )


class ActivityAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityAnswer
        fields = (
            'id', 'google_drive_file_key',
            'activity', 'student',
        )

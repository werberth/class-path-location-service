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
            'content', 'is_multimidia', 'create_at',
            'update_at'
        )


class ActivityAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityAnswer
        fields = (
            'id', 'file', 'type',
            'activity', 'student',
        )
        extra_kwargs = {'student': {'read_only': True}}

    def create(self, validated_data):
        validated_data.update({
            'student': self.context['request'].user.student
        })
        return super(ActivityAnswerSerializer, self).create(validated_data)

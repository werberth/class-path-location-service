from rest_framework import serializers

from class_path_content.accounts.models import Class
from ..models import Content, Activity, ActivityAnswer


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = (
            'id', 'title', 'description',
            'teacher', 'created_at', 'modified_at'
        )
        extra_kwargs = {'teacher': {'read_only': True}}

    def create(self, validated_data):
        validated_data.update({
            'teacher': self.context['request'].user.teacher
        })
        return super(ContentSerializer, self).create(validated_data)


class ContentSerializerReadOnly(serializers.ModelSerializer):
    class Meta:
        depth = 2
        model = Content
        fields = (
            'id', 'title', 'description', 'teacher',
            'teacher', 'created_at', 'modified_at'
        )


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = (
            'id', 'title', 'description', 'location',
            'content', 'class_id', 'multimedia_required', 'created_at',
            'modified_at'
        )
        extra_kwargs = {
            'content':  {'required': True, 'allow_null': False},
            'class_id': {'required': True, 'allow_null': False},
            'location': {'required': True, 'allow_null': False},
        }

    def get_fields(self):
        fields = super().get_fields()
        teacher = self.context['request'].user.teacher
        classes = teacher.courses.values_list('class_id__id', flat=True)

        fields['content'].queryset = teacher.contents.all()
        fields['class_id'].queryset = Class.objects.filter(id__in=classes)
        fields['location'].queryset = teacher.locations.all()

        return fields


class ActivitySerializerReadOnly(serializers.ModelSerializer):
    class Meta:
        depth = 2
        model = Activity
        fields = (
            'id', 'title', 'description', 'location',
            'content', 'class_id', 'multimedia_required', 'created_at',
            'modified_at'
        )


class ActivityAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityAnswer
        fields = (
            'id', 'file',
            'activity', 'student',
        )
        extra_kwargs = {'student': {'read_only': True}, 'file': {'read_only': True}}

    def create(self, validated_data):
        validated_data.update({
            'student': self.context['request'].user.student
        })
        return super(ActivityAnswerSerializer, self).create(validated_data)
 

class ActivityAnswerSerializerReadOnly(serializers.ModelSerializer):
    class Meta:
        depth = 2
        model = ActivityAnswer
        fields = (
            'id', 'file',
            'activity', 'student',
        )

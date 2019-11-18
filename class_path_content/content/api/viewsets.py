from rest_framework import serializers, viewsets, permissions

from ..models import Content, Activity, ActivityAnswer

from . import serializers, permissions as perms


class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = serializers.ContentSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        perms.OnlyTeachersCanEditOrStudentsCanRead
    )
    filterset_fields = ['course']

    def get_queryset(self):
        user = self.request.user
        if user.is_student:
            return user.student.contents
        elif user.is_teacher:
            return user.teacher.contents


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = serializers.ActivitySerializer
    permission_classes = (
        permissions.IsAuthenticated,
        perms.OnlyTeachersCanEditOrStudentsCanRead
    )
    filterset_fields = ['location', 'content']

    def get_queryset(self):
        user = self.request.user
        if user.is_student:
            return user.student.activities
        elif user.is_teacher:
            return user.teacher.activities

class ActivityAnswerViewSet(viewsets.ModelViewSet):
    queryset = ActivityAnswer.objects.all()
    serializer_class = serializers.ActivityAnswerSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        perms.OnlyStudentsCanEditOrTeachersCanRead
    )
    filterset_fields = ['type', 'activity']

    def get_queryset(self):
        user = self.request.user
        if user.is_teacher:
            return user.teacher.answers
        elif user.is_student:
            return user.student.answers

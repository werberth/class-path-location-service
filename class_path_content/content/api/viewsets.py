from rest_framework import serializers, viewsets, permissions, status
from rest_framework.response import Response

from ..models import Content, Activity, ActivityAnswer

from . import serializers, permissions as perms


class BaseDepthViewSet(viewsets.ModelViewSet):
    user_actions = ['list', 'retrieve']
    read_only_serializer_class = None

    def get_teachers(self):
        class_id = self.request.user.student.class_id

        if self.request.user.has_institution:
            teachers = class_id.courses.values_list('teacher', flat=True)
            return teachers

        return [class_id.teacher.id]


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        read_serializer = self.read_only_serializer_class(instance)
        headers = self.get_success_headers(read_serializer.data)
        return Response(
            read_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        serializer = self.read_only_serializer_class(self.get_object())
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.action in self.user_actions:
            return self.read_only_serializer_class
        return self.serializer_class


class ContentViewSet(BaseDepthViewSet):
    serializer_class = serializers.ContentSerializer
    read_only_serializer_class = serializers.ContentSerializerReadOnly

    permission_classes = (
        permissions.IsAuthenticated,
        perms.OnlyTeachersCanEditOrStudentsCanRead
    )

    def get_queryset(self):
        user = self.request.user
        if user.is_student:
            teachers = self.get_teachers()
            queryset = Content.objects.filter(teacher__id__in=teachers)

            teacher_filter = self.request.query_params.get('teacher')
            if teacher_filter:
                queryset = queryset.filter(teacher__id=teacher_filter)
            return queryset

        elif user.is_teacher:
            return user.teacher.contents.all()


class ActivityViewSet(BaseDepthViewSet):
    serializer_class = serializers.ActivitySerializer
    read_only_serializer_class = serializers.ActivitySerializerReadOnly

    permission_classes = (
        permissions.IsAuthenticated,
        perms.OnlyTeachersCanEditOrStudentsCanRead
    )

    def get_queryset(self):
        user = self.request.user

        if user.is_student and not user.has_institution:
            return Activity.objects.filter(class_id=user.student.class_id)

        if user.is_student:
            courses = user.student.class_id.courses.values_list('id', flat=True)
            return Activity.objects.filter(course__id__in=courses)

        if user.is_teacher:
            contents = user.teacher.contents.values_list('id', flat=True)
            return Activity.objects.filter(content__id__in=contents)


class ActivityAnswerViewSet(BaseDepthViewSet):
    serializer_class = serializers.ActivityAnswerSerializer
    read_only_serializer_class = serializers.ActivityAnswerSerializerReadOnly
    permission_classes = (
        permissions.IsAuthenticated,
        perms.OnlyStudentsCanEditOrTeachersCanRead
    )

    def get_queryset(self):
        user = self.request.user
        if user.is_teacher:
            contents = user.teacher.contents.values_list('id', flat=True)
            return ActivityAnswer.objects.filter(activity__content__id=contents)
        elif user.is_student:
            return user.student.answers.all()

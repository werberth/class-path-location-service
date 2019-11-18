from rest_framework import permissions


class OnlyStudents(permissions.BasePermission):
    message = 'Only students are allowed.'

    def has_permission(self, request, view):
        return request.user.is_student


class OnlyTeachers(permissions.BasePermission):
    message = 'Only teachers are allowed.'

    def has_permission(self, request, view):
        return request.user.is_teacher


class OnlyTeachersCanEditOrStudentsCanRead(permissions.BasePermission):
    message = 'Only teachers or students are allowed.'
    teacher_actions = ['update', 'partial_update', 'create', 'destroy']

    def has_permission(self, request, view):
        if view.action in self.teacher_actions:
            return request.user.is_teacher
        return request.user.is_teacher or request.user.is_student


class OnlyStudentsCanEditOrTeachersCanRead(permissions.BasePermission):
    message = 'Only teachers or students are allowed.'
    student_actions = ['update', 'partial_update', 'create', 'destroy']

    def has_permission(self, request, view):
        if view.action in self.student_actions:
            return request.user.is_student
        return request.user.is_teacher or request.user.is_student

from rest_framework import permissions


class OnlyStudents(permissions.BasePermission):
    message = 'Only students are allowed.'

    def has_permission(self, request, view):
        return request.user.is_student


class OnlyTeachers(permissions.BasePermission):
    message = 'Only teachers are allowed.'

    def has_permission(self, request, view):
        return request.user.is_teacher


class OnlyTeachersOrStudents(permissions.BasePermission):
    message = 'Only teachers or students are allowed.'

    def has_permission(self, request, view):
        return request.user.is_teacher or request.user.is_student

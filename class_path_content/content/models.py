from django.db import models

from ..accounts.models import Teacher, Student, Course
from ..location.models import Location


class Content(models.Model):
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name="contents"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="contents"
    )
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'content'
        managed = False

    def __str__(self):
        return self.title


class Activity(models.Model):
    title = models.CharField(max_length=250)
    description = models.CharField(max_length=250)
    location = models.ForeignKey(
        Location,
        on_delete=models.CASCADE,
        related_name="activities"
    )
    content = models.ForeignKey(
        Content,
        on_delete=models.CASCADE,
        related_name="activities"
    )
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'activity'
        managed = False

    def __str__(self):
        return self.title


class ActivityAnswer(models.Model):
    google_drive_file_key = models.CharField(max_length=200)
    activity = models.ForeignKey(
        Activity,
        on_delete=models.CASCADE,
        related_name="answers"
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="answers"
    )

    class Meta:
        db_table = 'activity_answer'
        managed = False

    def __str__(self):
        return f'{self.student.full_name}: {self.google_drive_file_key}'

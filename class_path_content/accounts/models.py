from django.contrib.auth.models import AbstractUser, Permission
from django.contrib.contenttypes.models import ContentType
from django.utils.functional import cached_property

from django.db import models

from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class User(AbstractUser):
    registration_number = models.CharField(
        _('registration number'),
        max_length=25,
        unique=True
    )
    email = models.EmailField(_('email address'), unique=True)
    is_teacher = models.BooleanField(_('is teacher'), default=False)
    is_student = models.BooleanField(_('is student'), default=False)

    objects = CustomUserManager()

    username = None

    USERNAME_FIELD = 'registration_number'

    class Meta:
        db_table = 'users'
        managed = False

    def __str__(self):
        return self.email


class Profile(models.Model):
    cpf = models.CharField(
        _('cpf'),
        max_length=100,
        default=None,
        null=True,
        blank=True
    )
    full_name = models.CharField(
        _('full name'),
        max_length=250,
        blank=True,
        null=True
    )
    description = models.TextField(_('description'), blank=True, null=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    modified_at = models.DateTimeField(_('modified at'), auto_now=True)

    class Meta:
        abstract = True
        managed = False

    def __str__(self):
        return self.full_name or self.user.email


class Institution(models.Model):
    name = models.CharField(_('name'), max_length=250)
    description = models.TextField(_('description'), blank=True, null=True)
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)
    modified_at = models.DateTimeField(_('modified_at'), auto_now=True)

    class Meta:
        db_table = 'institution'
        managed = False

    def __str__(self):
        return self.name


class Program(models.Model):
    name = models.CharField(_('name'), max_length=200)
    description = models.TextField(_('description'), blank=True, null=True)
    institution = models.OneToOneField(Institution, on_delete=models.CASCADE)
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)
    modified_at = models.DateTimeField(_('modified_at'), auto_now=True)

    class Meta:
        db_table = 'program'
        managed = False

    def __str__(self):
        return self.name


class Class(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    program = models.ForeignKey(
        Program,
        on_delete=models.CASCADE,
        related_name="classes"
    )
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)
    modified_at = models.DateTimeField(_('modified_at'), auto_now=True)

    class Meta:
        db_table = 'class'
        managed = False

    def __str__(self):
        return self.name


class Admin(Profile):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="admin"
    )
    institution = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE,
        related_name="admins",
        null=True,
    )
    class Meta:
        db_table = 'admin'
        managed = False


class Teacher(Profile):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="teacher"
    )
    institution = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE,
        related_name="teachers"
    )
    class Meta:
        db_table = 'teacher'
        managed = False

    @cached_property
    def contents(self):
        return self.courses.all()

    @cached_property
    def activities(self):
        from ..content.models import Activity

        queryset = Activity.objects.filter(content__teacher__id=self.id)
        return queryset

    @cached_property
    def answers(self):
        from ..content.models import ActivityAnswer

        queryset = ActivityAnswer.objects.filter(
            activity__content__teacher__id=self.id
        )
        return queryset


class Student(Profile):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="student"
    )
    class_id = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        related_name="students"
    )

    class Meta:
        db_table = 'student'
        managed = False

    @cached_property
    def contents(self):
        from ..content.models import Content

        queryset = Content.objects.filter(courses__class_id=self.class_id)
        return queryset

    @cached_property
    def activity(self):
        from ..content.models import Activity

        queryset = Activity.objects.filter(
            content__course__class_id=self.class_id
        )
        return queryset

    @cached_property
    def answers(self):
        from ..content.models import ActivityAnswer

        queryset = ActivityAnswer.objects.filter(
            activity__content__course__class_id=self.class_id
        )
        return queryset


class Address(models.Model):
    state = models.CharField(_('state'), max_length=2)
    city = models.CharField(_('city'), max_length=100)
    street = models.CharField(_('street'), max_length=250)
    neighborhood = models.CharField(_('neighborhood'), max_length=100)
    number = models.IntegerField(_('number'))
    postal_code = models.CharField(_('postal_code'), max_length=250)
    complement = models.CharField(
        _('complement'),
        max_length=250,
        blank=True,
        null=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='addresses'
    )
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)
    modified_at = models.DateTimeField(_('modified_at'), auto_now=True)

    class Meta:
        db_table = 'address'
        managed = False

    def __str__(self):
       return f'{self.street} {self.number}, {self.postal_code}'


class Course(models.Model):
    name = models.CharField(_('name'), max_length=200)
    description = models.TextField(_('description'), blank=True, null=True)
    class_id = models.ForeignKey(
        Class,
        on_delete=models.CASCADE,
        related_name="courses"
    )
    teacher = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name="courses"
    )
    program = models.ForeignKey(
        Program,
        on_delete=models.CASCADE,
        related_name="courses"
    )
    created_at = models.DateTimeField(_('created_at'), auto_now_add=True)
    modified_at = models.DateTimeField(_('modified_at'), auto_now=True)

    class Meta:
        db_table = 'course'

    def __str__(self):
        return self.name
        managed = False
from django.contrib.auth.models import AbstractUser, Permission
from django.contrib.contenttypes.models import ContentType

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

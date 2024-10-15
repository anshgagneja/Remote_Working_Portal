from builtins import property

from django.contrib.auth.models import (AbstractBaseUser,BaseUserManager)
from django.db import models
from django.contrib.auth.models import PermissionsMixin
class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email )
        user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    email = models.EmailField(max_length=255,unique=True)
    full_name = models.CharField(max_length=250,blank=True,null=True)
    teacher = models.BooleanField(default=True)
    student = models.BooleanField(default=False)
    college_name = models.CharField(max_length=225,blank=True,null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = MyUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.full_name

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_teacher(self):
        return self.teacher

    @property
    def is_student(self):
        return self.student

class Assignment(models.Model):
    title = models.CharField(max_length=255)
    upload = models.FileField(upload_to='assignments/', null=True, default="No file uploaded",blank=True)
    due_date = models.DateField()
    created_at = models.DateField(auto_now_add=True)
    last_updated = models.DateField(auto_now=True)
    active = models.BooleanField(default=True)
    course_code = models.CharField(max_length=8)
    course_title = models.CharField(max_length=255)
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='assignments'
    )

    def __str__(self):
        return self.title

class Submission(models.Model):
    description = models.CharField(max_length=100, null=True, blank=True, default="No description")
    upload = models.FileField(upload_to='submissions/',blank=True)
    submitted_at = models.DateField(default=None)
    last_updated = models.DateField(auto_now=True)
    active = models.BooleanField(default=True)
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name='submissions'
    )

    def __str__(self):
        return str(self.assignment_id)


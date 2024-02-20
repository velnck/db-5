from django.contrib.auth.models import UserManager
from django.db import models

from users.roles import get_admin_role_id, get_employee_role_id, get_customer_role_id


class Users(models.Model):
    REQUIRED_FIELDS = ('password',)
    USERNAME_FIELD = 'username'

    id = models.IntegerField(blank=True, null=False, primary_key=True)
    username = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=256)
    name = models.CharField(max_length=256, blank=True, null=True)
    phone_number = models.CharField()
    is_active = models.BooleanField(blank=True, null=True)
    role = models.ForeignKey('Roles', models.SET_NULL, null=True)

    class Meta:
        managed = False
        db_table = 'users'

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    @property
    def is_superuser(self):
        return self.role.id == get_admin_role_id()

    @property
    def is_staff(self):
        return (self.role.id == get_employee_role_id()
                or self.role.id == get_admin_role_id())

    objects = UserManager()


class Roles(models.Model):
    id = models.IntegerField(blank=True, null=False, primary_key=True)
    name = models.CharField(unique=True, max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roles'


class Logs(models.Model):
    id = models.IntegerField(blank=True, null=False, primary_key=True)
    user = models.ForeignKey(Users, models.RESTRICT)
    time = models.DateTimeField()
    message = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'logs'

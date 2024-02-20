from django.db import models

from users.models import Users


class Orders(models.Model):
    id = models.IntegerField(blank=True, null=False, primary_key=True)
    delivery_address = models.CharField(blank=True, null=True)
    creation_date = models.DateTimeField(blank=True, null=True)
    delivery_date = models.DateField(blank=True, null=True)
    user = models.ForeignKey(Users, models.DO_NOTHING)
    sum_total = models.DecimalField(max_digits=10, decimal_places=5, blank=True, null=True, default=0)
    is_commited = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders'

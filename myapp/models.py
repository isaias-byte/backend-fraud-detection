# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Transactions(models.Model):
    id = models.BigAutoField(primary_key=True)
    distance_from_home = models.CharField(max_length=255, blank=True, null=True)
    distance_from_last_transaction = models.CharField(max_length=255, blank=True, null=True)
    ratio_to_median_purchase_price = models.CharField(max_length=255, blank=True, null=True)
    repeat_retailer = models.IntegerField(blank=True, null=True)
    used_chip = models.IntegerField(blank=True, null=True)
    used_pin_number = models.IntegerField(blank=True, null=True)
    online_order = models.IntegerField(blank=True, null=True)
    fraud = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transactions'

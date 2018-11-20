# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class Food(models.Model):
    food_id = models.AutoField(primary_key=True)
    price = models.DecimalField(max_digits=38, decimal_places=2)
    description = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(unique=True, max_length=30)
    food_type = models.ForeignKey('FoodType', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'food'

    def __str__(self):
        return str(self.food_id) + " - " + self.title


class FoodType(models.Model):
    type_id = models.AutoField(primary_key=True)
    type_name = models.CharField(unique=True, max_length=20)

    class Meta:
        managed = False
        db_table = 'food_type'

    def __str__(self):
        return str(self.type_id) + " - " + self.type_name
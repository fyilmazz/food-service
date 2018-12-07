# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AuthUser(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    password = models.CharField(max_length=128, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


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


class Client(models.Model):
    client_id = models.BigIntegerField(primary_key=True)
    username = models.CharField(unique=True, max_length=50)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=11)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'client'


class Cart(models.Model):
    cart_id = models.BigIntegerField(primary_key=True)
    client = models.ForeignKey('Client', models.DO_NOTHING)
    valid = models.BigIntegerField()
    client_u = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cart'
        unique_together = (('client_u', 'valid'),)


class Cart2Food(models.Model):
    c2f_id = models.BigIntegerField(primary_key=True)
    cart = models.ForeignKey(Cart, models.DO_NOTHING)
    food = models.ForeignKey('Food', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'cart2food'


class FoodOrder(models.Model):
    order_id = models.BigIntegerField(primary_key=True)
    total_price = models.DecimalField(max_digits=38, decimal_places=2)
    order_date = models.DateField()
    payment_type = models.CharField(max_length=30)
    order_address = models.CharField(max_length=100)
    cart = models.ForeignKey('Cart', models.DO_NOTHING, unique=True)

    class Meta:
        managed = False
        db_table = 'food_order'

    def __str__(self):
        foods = ", ".join(str(i[0]) for i in Cart2Food.objects.filter(cart=self.cart).values_list('food__title'))
        return foods + " - " + str(self.total_price) + " Lira - " + self.payment_type + " - " + str(self.order_date) + " - " + self.order_address

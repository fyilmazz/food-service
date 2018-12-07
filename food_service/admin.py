from django.contrib import admin
from food_service.models import *


admin.site.register([Food, FoodType, FoodOrder])


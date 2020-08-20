
# Django
from django.contrib import admin

# local Django
from .models import DayName, Plan, Recipe, RecipePlan

# Register your models here.


admin.site.register(DayName)
admin.site.register(Plan)
admin.site.register(Recipe)
admin.site.register(RecipePlan)

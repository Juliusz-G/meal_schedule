
# Django
from django.views import View
from django.shortcuts import render

# local Django
from .models import Recipe

# third part
import random

# Create your views here.


class LandingPage(View):

    def get(self, request):
        first_recipe = random.choice(Recipe.objects.all().values('id'))
        first = Recipe.objects.get(**first_recipe)
        second_recipe = random.choice(Recipe.objects.all().values('id'))
        second = Recipe.objects.get(**second_recipe)
        third_recipe = random.choice(Recipe.objects.all().values('id'))
        third = Recipe.objects.get(**third_recipe)
        ctx = {
            'first': first,
            'second': second,
            'third': third
        }
        return render(request, "index.html", ctx)


class Dashboard(View):

    def get(self, request):
        return render(request, "dashboard.html", {})


class RecipePage(View):

    def get(self, request):
        return render(request, "app-recipes.html", {})
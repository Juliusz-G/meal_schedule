# Django
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View

# local Django
from .models import DayName, Plan, Recipe, RecipePlan

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
        all_recipes = Recipe.objects.count()
        all_plans = Plan.objects.count()
        last_plan = Plan.objects.last()
        # recipe_plan = RecipePlan.objects.all().order_by('-id')[0]
        ctx = {"all_recipes": all_recipes,
               "all_plans": all_plans,
               "last_plan": last_plan,
               # "recipe_plan": recipe_plan,
               # "meal_name": recipe_plan.meal_name,
               # "order": recipe_plan.order,
               # "plan_name": Plan.objects.get(id=recipe_plan.plan_id),
               # "recipe_name": Recipe.objects.get(id=recipe_plan.recipe_id),
               # "recipe_id": recipe_plan.recipe_id,
               # "day_name": DayName.objects.get(id=recipe_plan.dayname_id),
               "days": DayName.objects.all(),
               }
        return render(request, "dashboard.html", ctx)


class RecipePage(View):

    def get(self, request):
        recipes = Recipe.objects.order_by('-votes')
        paginator = Paginator(recipes, 2)
        page = request.GET.get('page')
        recipe = paginator.get_page(page)
        return render(request, "app-recipes.html", {"recipe": recipe})


class AddRecipe(View):

    def get(self, request):
        return render(request, "app-add-recipe.html")

    def post(self, request):
        name = request.POST.get("name")
        description = request.POST.get("description")
        preparation_time = request.POST.get("preparation_time")
        preparation_description = request.POST.get("preparation_description")
        ingredients = request.POST.get("ingredients")
        if name and description and preparation_time and preparation_description and ingredients is not None:
            recipe = Recipe.objects.create(name=name, description=description, preparation_time=int(preparation_time),
                                           preparation_description=preparation_description, ingredients=ingredients)
            recipe.save()
            response = redirect(reverse_lazy('app-recipes'))
            return response
        else:
            warning = "Wypełnij poprawnie wszystkie pola"
            ctx = {'warning': warning}
            return render(request, "app-add-recipe.html", ctx)

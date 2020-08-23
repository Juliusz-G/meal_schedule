# Django
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
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
        preparation_method = request.POST.get("preparation_method")
        preparation_time = request.POST.get("preparation_time")
        ingredients = request.POST.get("ingredients")
        if name and description and preparation_time and preparation_method and ingredients is not None:
            recipe = Recipe.objects.create(name=name, description=description, preparation_method=preparation_method,
                                           preparation_time=int(preparation_time), ingredients=ingredients)
            recipe.save()
            response = redirect(reverse_lazy('app-recipes'))
            return response
        else:
            warning = "Wypełnij poprawnie wszystkie pola"
            ctx = {'warning': warning}
            return render(request, "app-add-recipe.html", ctx)


class RecipeDetails(View):

    def get(self, request, recipe_id):
        recipe = Recipe.objects.get(pk=recipe_id)

        ctx = {
            "name": recipe.name,
            "description": recipe.description,
            "preparation_method": recipe.preparation_method,
            "ingredients": recipe.ingredients,
            "preparation_time": recipe.preparation_time,
            "vote": recipe.votes
        }
        return render(request, "app-recipe-details.html", ctx)

    def post(self, request, recipe_id):
        recipe = Recipe.objects.get(pk=recipe_id)
        if request.POST.get('like') == 'Polub przepis':
            recipe.votes += 1
            recipe.save()
        elif request.POST.get('dislike') == 'Nie lubię przepisu':
            recipe.votes -= 1
            recipe.save()

        ctx = {
            "name": recipe.name,
            "description": recipe.description,
            "preparation_method": recipe.preparation_method,
            "ingredients": recipe.ingredients,
            "preparation_time": recipe.preparation_time,
            "vote": recipe.votes
        }
        return render(request, "app-recipe-details.html", ctx)


class EditRecipe(View):

    def get(self, request, recipe_id):
        recipe = Recipe.objects.get(pk=recipe_id)
        ctx = {
            "id": recipe.pk,
            "name": recipe.name,
            "description": recipe.description,
            "ingredients": recipe.ingredients,
            "preparation_time": recipe.preparation_time,
            "preparation_method": recipe.preparation_method,
            "vote": recipe.votes
        }
        return render(request, "app-edit-recipe.html", ctx)

    def post(self, request, recipe_id):
        name = request.POST.get("name")
        description = request.POST.get("description")
        preparation_time = request.POST.get("preparation_time")
        preparation_method = request.POST.get("preparation_method")
        ingredients = request.POST.get("ingredients")
        if name and description and preparation_time and preparation_method and ingredients is not None:
            Recipe.objects.filter(pk=recipe_id).update(name=name, ingredients=ingredients, description=description,
                                                       preparation_time=int(preparation_time),
                                                       preparation_method=preparation_method)

            response = redirect(reverse_lazy('app-recipes'))
            return response

        else:
            recipe = Recipe.objects.get(pk=recipe_id)
            warning = "Wypełnij poprawnie wszystkie pola!"
            ctx = {
                "id": recipe.pk,
                "name": recipe.name,
                "description": recipe.description,
                "ingredients": recipe.ingredients,
                "preparation_time": recipe.preparation_time,
                "preparation_method": recipe.preparation_method,
                "vote": recipe.votes,
                "warning": warning
            }
            return render(request, "app-edit-recipe.html", ctx)


class DeleteRecipe(View):

    def get(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        ctx = {
            "name": recipe.name
        }
        return render(request, "app-delete-recipe.html", ctx)

    def post(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        recipe.delete()
        response = redirect('../')
        return response

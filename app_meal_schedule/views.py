# Django
from django.core.paginator import Paginator
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View

# local Django
from .models import DayName, Plan, Recipe, RecipePlan, Days

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


class SchedulePage(View):

    def get(self, request):
        plans = Plan.objects.all()
        paginator = Paginator(plans, 2)
        page = request.GET.get('page')
        plan = paginator.get_page(page)
        return render(request, "app-schedules.html", {"plan": plan})


class AddSchedule(View):

    def get(self, request):
        return render(request, "app-add-schedules.html")

    def post(self, request):
        name = request.POST.get("name")
        description = request.POST.get("description")
        if name and description:
            plan = Plan.objects.create(name=name, description=description)
            plan.save()
            response = redirect('/plan/list')
            return response

        else:
            warning = "Wypełnij poprawnie wszystkie pola"
            ctx = {'warning': warning}
            return render(request, "app-add-schedules.html", ctx)


class ScheduleDetails(View):

    def get(self, request, recipe_plan_id):
        recipe_plan = RecipePlan.objects.get(pk=recipe_plan_id)

        ctx = {
            "RecipePlan": recipe_plan,
            "meal_name": recipe_plan.meal_name,
            "order": recipe_plan.order,
            "plan_name": Plan.objects.get(id=recipe_plan.Plan_id),
            "recipe_name": Recipe.objects.get(id=recipe_plan.Recipe_id),
            "recipe_id": recipe_plan.Recipe_id,
            "day_name": DayName.objects.get(id=recipe_plan.DayName_id),
            "days": DayName.objects.all(),
        }

        return render(request, "app-details-schedules.html", ctx)


class EditSchedule(View):

    def get(self, request, plan_id):
        plan = Plan.objects.get(pk=plan_id)

        ctx = {
            "plan_name": plan.name,
            "plan_description": plan.description
        }
        return render(request, "app-edit-schedules.html", ctx)

    def post(self, request, plan_id):
        plan_name = request.POST.get("plan_name")
        plan_description = request.POST.get("plan_description")
        if plan_name and plan_description:
            Plan.objects.filter(pk=plan_id).update(name=plan_name, description=plan_description)

            response = redirect('/plan/list')
            return response

        else:
            plan = Plan.objects.get(pk=plan_id)
            warning = "Wypełnij poprawnie wszystkie pola"

            ctx = {
                "warning": warning,
                "plan_name": plan.name,
                "plan_description": plan.description
            }
            return render(request, "app-edit-schedules.html", ctx)


class DeleteSchedule(View):

    def get(self, request, plan_id):
        plan = get_object_or_404(Plan, pk=plan_id)
        ctx = {
            "name": plan.name
        }
        return render(request, "app-delete-schedule.html", ctx)

    def post(self, request, plan_id):
        plan = get_object_or_404(Plan, pk=plan_id)
        plan.delete()
        response = redirect('/plan/list/')
        return response


class AddRecipeToSchedulesDashboard(View):

    def get(self, request):
        plans = Plan.objects.all()
        recipes = Recipe.objects.all()
        days = DayName.objects.all()
        ctx = {
            "plans": plans,
            "recipes": recipes,
            "days": days
        }
        return render(request, "app-schedules-meal-recipe.html", ctx)

    def post(self, request):
        meal_name = request.POST.get("meal_name")
        order = request.POST.get("order_id")
        recipe_id = request.POST.get("recipe_id")
        plan_id = request.POST.get("plan_id")
        day_id = request.POST.get("day_id")

        recipe = Recipe.objects.get(name=recipe_id)
        plan = Plan.objects.get(name=plan_id)
        day = DayName.objects.get(name=day_id)

        if meal_name and order and recipe_id and plan_id and day_id:
            m = RecipePlan.objects.create(meal_name=meal_name, order=order, Plan=plan,
                                          Recipe=recipe, DayName=day)
            m.save()
            return redirect(f"/plan/add-recipe/")

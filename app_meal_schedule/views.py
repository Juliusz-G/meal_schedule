
# Django
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View

# local Django
from .models import DayName, Plan, Recipe, RecipePlan

# third part
import random


# Create your views here.


class Login(View):
    """Login a user."""

    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect(reverse_lazy("dashboard"))
            else:
                return HttpResponse("Błędne dane.")
        else:
            warning = "Użytjownik nie istnieje."
            ctx = {"warning": warning}
            return render(request, "login.html", ctx)


class Logout(View):
    """Simply logs out a user and redirects to landing page."""

    def get(self, request):
        logout(request)
        return redirect(reverse_lazy("landing-page"))


class Register(View):
    """Creates user and saves to db."""

    def get(self, request):
        return render(request, "register.html")

    def post(self, request):
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        if first_name and last_name and username and password1 and password2 is not None:
            if password1 == password2:
                user = User.objects.create(first_name=first_name, last_name=last_name, username=username,
                                           password=password1)
                user.set_password(password1)
                user.save()
                response = redirect(reverse_lazy("login"))
                return response
        else:
            warning = "Wypełnij poprawnie wszystkie pola"
            ctx = {"warning": warning}
            return render(request, "register.html", ctx)


class ResetPassword(View):
    """Reset user password."""

    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        return render(request, "reset-password.html")

    def post(self, request, user_id):
        new_password1 = request.POST.get("new_password1")
        new_password2 = request.POST.get("new_password2")
        if new_password1 and new_password2 is not None:
            if new_password1 == new_password1:
                user = get_object_or_404(User, pk=user_id)
                user.set_password(new_password1)
                user.save()
                logout(request)
                return redirect(reverse_lazy("login"))
        else:
            warning = "Wypełnij poprawnie wszystkie pola"
            ctx = {"warning": warning}
            return render(request, "reset-password.html", ctx)


class ProfileEdit(View):
    """Displays user profil edit form and saves data."""

    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        return render(request, "profile-edit.html", {"user": user})

    def post(self, request, user_id):
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        if first_name and last_name is not None:
            get_object_or_404(User, pk=user_id)
            user = User.objects.update(first_name=first_name, last_name=last_name)
            user.save()
            return redirect(reverse_lazy("dashboard"))
        else:
            warning = "Wypełnij poprawnie wszystkie pola"
            ctx = {"warning": warning}
            return render(request, "profile-edit.html", ctx)


class LandingPage(View):
    """Displays landing page. Slides with recipes from db."""

    def get(self, request):
        first_recipe = random.choice(Recipe.objects.all().values('id'))
        first = Recipe.objects.get(**first_recipe)
        second_recipe = random.choice(Recipe.objects.all().values('id'))
        second = Recipe.objects.get(**second_recipe)
        third_recipe = random.choice(Recipe.objects.all().values('id'))
        third = Recipe.objects.get(**third_recipe)
        ctx = {
            "first": first,
            "second": second,
            "third": third
        }
        return render(request, "index.html", ctx)


class Dashboard(View):
    """Displays dashboard with several data (amount of recipes, amount of plans,
    name of last plan added and whole last plan).
    """

    def get(self, request):
        recipes = Recipe.objects.count()
        plans = Plan.objects.count()
        last_plan = Plan.objects.last()
        days = DayName.objects.all()
        if last_plan is None:
            last_plan = "Brak ostatniego planu!"
            days = {}
        ctx = {
            "recipes": recipes,
            "plans": plans,
            "last_plan": last_plan,
            "days": days,
        }
        return render(request, "dashboard.html", ctx)


class RecipeList(View):
    """Shows list of recipes with paginator, sorted by votes."""

    def get(self, request):
        recipes = Recipe.objects.order_by("-votes", "id")
        paginator = Paginator(recipes, 2)
        page = request.GET.get("page")
        recipe = paginator.get_page(page)
        return render(request, "recipes.html", {"recipe": recipe})


class RecipeAdd(View):
    """Displays a recipe add form."""

    def get(self, request):
        return render(request, "recipe-add.html")

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
            response = redirect(reverse_lazy("recipes"))
            return response
        else:
            warning = "Wypełnij poprawnie wszystkie pola"
            ctx = {"warning": warning}
            return render(request, "recipe-add.html", ctx)


class RecipeDetails(View):
    """Shows recipe details, whole data from form."""

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
        return render(request, "recipe-details.html", ctx)

    def post(self, request, recipe_id):
        recipe = Recipe.objects.get(pk=recipe_id)
        if request.POST.get("like") == "Polub przepis":
            recipe.votes += 1
            recipe.save()
        elif request.POST.get("dislike") == "Nie lubię przepisu":
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
        return render(request, "recipe-details.html", ctx)


class RecipeEdit(View):
    """Displays 'RecipeDetails' and makes it editable."""

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
        return render(request, "recipe-edit.html", ctx)

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
            response = redirect(reverse_lazy("recipes"))
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
            return render(request, "recipe-edit.html", ctx)


class RecipeDelete(View):
    """Deletes a recipe from database."""

    def get(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        ctx = {
            "name": recipe.name
        }
        return render(request, "recipe-delete.html", ctx)

    def post(self, request, recipe_id):
        recipe = get_object_or_404(Recipe, pk=recipe_id)
        recipe.delete()
        response = redirect("../")
        return response


class ScheduleList(View):
    """Displays list of schedules with paginator."""

    def get(self, request):
        plans = Plan.objects.order_by("id")
        paginator = Paginator(plans, 2)
        page = request.GET.get("page")
        plan = paginator.get_page(page)
        return render(request, "schedules.html", {"plan": plan})


class ScheduleAdd(View):
    """Displays a schedule add form."""

    def get(self, request):
        return render(request, "schedule-add.html")

    def post(self, request):
        name = request.POST.get("name")
        description = request.POST.get("description")
        if name and description:
            plan = Plan.objects.create(name=name, description=description)
            plan.save()
            response = redirect(reverse_lazy("schedules"))
            return response
        else:
            warning = "Wypełnij poprawnie wszystkie pola"
            ctx = {"warning": warning}
            return render(request, "schedule-add.html", ctx)


class ScheduleDetails(View):
    """Show schedule details."""

    def get(self, request, plan_id):
        plan = Plan.objects.get(pk=plan_id)
        days = DayName.objects.all()
        ctx = {
            "plan": plan,
            "days": days,
        }
        return render(request, "schedule-details.html", ctx)


class ScheduleEdit(View):
    """Enable to edit existing schedule form."""

    def get(self, request, plan_id):
        plan = Plan.objects.get(pk=plan_id)
        ctx = {
            "plan_name": plan.name,
            "plan_description": plan.description
        }
        return render(request, "schedule-edit.html", ctx)

    def post(self, request, plan_id):
        plan_name = request.POST.get("plan_name")
        plan_description = request.POST.get("plan_description")
        if plan_name and plan_description:
            Plan.objects.filter(pk=plan_id).update(name=plan_name, description=plan_description)
            response = redirect(reverse_lazy("schedules"))
            return response
        else:
            plan = Plan.objects.get(pk=plan_id)
            warning = "Wypełnij poprawnie wszystkie pola"
            ctx = {
                "warning": warning,
                "plan_name": plan.name,
                "plan_description": plan.description
            }
            return render(request, "schedule-edit.html", ctx)


class ScheduleDelete(View):
    """Deletes schedule from database."""

    def get(self, request, plan_id):
        plan = get_object_or_404(Plan, pk=plan_id)
        ctx = {
            "name": plan.name
        }
        return render(request, "schedule-delete.html", ctx)

    def post(self, request, plan_id):
        plan = get_object_or_404(Plan, pk=plan_id)
        plan.delete()
        response = redirect(reverse_lazy("schedules"))
        return response


class AddRecipeToSchedule(View):
    """Adds recipe to selected schedule."""

    def get(self, request):
        plans = Plan.objects.all()
        recipes = Recipe.objects.all()
        days = DayName.objects.all()
        ctx = {
            "plans": plans,
            "recipes": recipes,
            "days": days
        }
        return render(request, "add-recipe-to-schedule.html", ctx)

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
            recipe_plan = RecipePlan.objects.create(meal_name=meal_name, order=order, Plan=plan,
                                                    Recipe=recipe, DayName=day)
            recipe_plan.save()
            return redirect(reverse_lazy("add-recipe-to-schedule"))


class DeleteRecipeFromSchedule(View):
    """Delete recipe from selected schedule."""

    def get(self, request, order_id):
        recipe_in_plan = get_object_or_404(RecipePlan.objects.all().filter(order__isnull=False), pk=order_id)
        ctx = {
            "recipe_name": recipe_in_plan.Recipe
        }
        return render(request, "delete-recipe-from-schedule.html", ctx)

    def post(self, request, order_id):
        plan_recipe = get_object_or_404(RecipePlan.objects.all().filter(order__isnull=False), pk=order_id)
        plan_recipe.delete()
        response = redirect("dashboard")
        return response

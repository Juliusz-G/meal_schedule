"""meal_schedule URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Django
from django.contrib import admin
from django.urls import path

# local Django
from app_meal_schedule.views import LandingPage, Dashboard, RecipePage, AddRecipe, RecipeDetails, EditRecipe, \
    DeleteRecipe, SchedulePage

urlpatterns = [
    # ADMIN
    path('admin/', admin.site.urls),

    # MAIN
    path('', LandingPage.as_view(), name='landing-page'),

    # DASHBOARD
    path('main/', Dashboard.as_view(), name='dashboard'),

    # RECIPE
    path('recipe/list/', RecipePage.as_view(), name='app-recipes'),
    path('recipe/add/', AddRecipe.as_view(), name='app-add-recipe'),
    path('recipe/<int:recipe_id>', RecipeDetails.as_view(), name='app-recipe-details'),
    path('recipe/edit/<int:recipe_id>', EditRecipe.as_view(), name='app-edit-recipe'),
    path('recipe/list/delete/<int:recipe_id>', DeleteRecipe.as_view(), name='app-delete-recipe'),

    # PLAN
    path('plan/list/', SchedulePage.as_view(), name='app-schedules'),
]

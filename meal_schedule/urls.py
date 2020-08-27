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
from app_meal_schedule.views import AddRecipeToSchedule, Dashboard, DeleteRecipeFromSchedule, LandingPage, Login, \
    Logout, ProfileEdit, RecipeAdd, RecipeDetails, RecipeDelete, RecipeEdit, RecipeList, Register, ResetPassword, \
    ScheduleAdd, ScheduleDetails, ScheduleDelete, ScheduleEdit, ScheduleList

urlpatterns = [
    # ADMIN
    path('admin/', admin.site.urls),

    # MAIN
    path('', LandingPage.as_view(), name='landing-page'),

    # DASHBOARD
    path('main/', Dashboard.as_view(), name='dashboard'),

    # RECIPE
    path('recipe/list/', RecipeList.as_view(), name='recipes'),
    path('recipe/add/', RecipeAdd.as_view(), name='recipe-add'),
    path('recipe/<int:recipe_id>', RecipeDetails.as_view(), name='recipe-details'),
    path('recipe/edit/<int:recipe_id>', RecipeEdit.as_view(), name='recipe-edit'),
    path('recipe/list/delete/<int:recipe_id>', RecipeDelete.as_view(), name='recipe-delete'),

    # PLAN
    path('plan/list/', ScheduleList.as_view(), name='schedules'),
    path('plan/add/', ScheduleAdd.as_view(), name='schedule-add'),
    path('plan/<int:plan_id>', ScheduleDetails.as_view(), name='schedule-details'),
    path('plan/edit/<int:plan_id>', ScheduleEdit.as_view(), name='schedule-edit'),
    path('plan/list/delete/<int:plan_id>', ScheduleDelete.as_view(), name='schedule-delete'),

    # RECIPE PLAN
    path('plan/add-recipe/', AddRecipeToSchedule.as_view(), name='add-recipe-to-schedule'),
    path('plan/delete-recipe/<int:order_id>', DeleteRecipeFromSchedule.as_view(),
         name='delete-recipe-from-schedule'),

    # USER
    path('login/', Login.as_view(), name="login"),
    path('logout/', Logout.as_view(), name="logout"),
    path('register/', Register.as_view(), name="register"),
    path('user/reset-password/<int:user_id>', ResetPassword.as_view(), name="reset-password"),
    path('user/edit-profile/<int:user_id>', ProfileEdit.as_view(), name="profile-edit"),
]

# Django
from django.db import models

# Create your models here.


Days = (
    ('pn', 'Poniedziałek'),
    ('wt', 'Wtorek'),
    ('śr', 'Środa'),
    ('cz', 'Czwartek'),
    ('pt', 'Piątek'),
    ('so', 'Sobota'),
    ('ni', 'Niedziela')
)


class Recipe(models.Model):
    name = models.CharField(max_length=128, verbose_name='Nazwa')
    ingredients = models.TextField(verbose_name='Składniki')
    description = models.TextField(verbose_name='Opis')
    preparation_method = models.TextField(verbose_name='Sposób przygotowania', null=True)
    created = models.DateField(auto_now_add=True, verbose_name='Stworzone')
    updated = models.DateField(auto_now_add=True, verbose_name='Zaktualizowane')
    preparation_time = models.PositiveIntegerField(verbose_name='Czas przygotowania')
    votes = models.PositiveIntegerField(default=0, verbose_name='Głosy')

    def __str__(self):
        return self.name


class DayName(models.Model):
    name = models.CharField(max_length=2, choices=Days, default="pn", verbose_name='Dzień')
    order = models.TextField(unique=True)

    def __str__(self):
        return self.name


class Plan(models.Model):
    name = models.CharField(max_length=128, verbose_name='Nazwa')
    description = models.TextField(verbose_name='Opis')
    created_data = models.DateField(auto_now_add=True, verbose_name='Stworzone')
    recipes = models.ManyToManyField(Recipe, through="RecipePlan")

    def __str__(self):
        return self.name


class RecipePlan(models.Model):
    Recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    Plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    meal_name = models.TextField()
    order = models.TextField(unique=True)
    DayName = models.ForeignKey(DayName, on_delete=models.CASCADE)

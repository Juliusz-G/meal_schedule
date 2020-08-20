
# Django
from django.db import models

# Create your models here.


class Recipe(models.Model):
    name = models.CharField(max_length=128, verbose_name='Nazwa')
    ingredients = models.TextField(verbose_name='Składniki')
    description = models.TextField(verbose_name='Opis')
    created = models.DateField(auto_now_add=True, verbose_name='Stworzone')
    updated = models.DateField(auto_now_add=True, verbose_name='Zaktualizowane')
    preparation_time = models.PositiveIntegerField(verbose_name='Czas przygotowania')
    votes = models.PositiveIntegerField(default=0, verbose_name='Głosy')

    def __str__(self):
        return self.name

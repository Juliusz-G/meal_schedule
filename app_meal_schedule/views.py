
# Django
from django.views import View
from django.shortcuts import render

# Create your views here.


class LandingPage(View):

    def get(self, request):
        return render(request, "index.html", {})

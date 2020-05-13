# Create your views here.
from django.shortcuts import render

from .models import *


def mainpage(request):
    # data = Country.objects.Last()

    stu = {
        "Country": {
            'Infected': 1000,
            'Recovered': 1,
            'Dead':  10
        }
    }
    return render(request, "mainpage/mainpage.html", stu)

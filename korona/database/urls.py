from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.mainpage, name="korona"),
    path('wykres', views.wykres, name="wykres")
]

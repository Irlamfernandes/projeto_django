from django.urls import path
from . import views

urlpatterns = [
    path('', views.buscar_filme, name = 'buscar_filme'),
]
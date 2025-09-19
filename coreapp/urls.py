from django.urls import path
from . import views

urlpatterns = [
    path("buscar/", views.BuscarFilmeView.as_view(), name = 'buscar_filme'),
]

from django.urls import path
from .views import BuscarFilmeView
from django.views.generic import TemplateView

urlpatterns = [
    path('resultados/', BuscarFilmeView.as_view(), name='resultados'),
    path('buscar/', BuscarFilmeView.as_view(), name='buscar'),
    path('index/', TemplateView.as_view(template_name='coreapp/index.html'), name='index'),
]
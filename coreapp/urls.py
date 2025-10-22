
from django.urls import path
from .views import BuscarFilmeView,SobreView, DetalheFilmeView, FilmesPopularesView
from django.views.generic import TemplateView

urlpatterns = [
    path('resultados/', BuscarFilmeView.as_view(), name='resultados'),
    path('buscar/', BuscarFilmeView.as_view(), name='buscar'),
    path('', TemplateView.as_view(template_name='coreapp/index.html'), name='index'),
    path('index/', TemplateView.as_view(template_name='coreapp/index.html'), name='index'),
    path('sobre/', SobreView.as_view(template_name='coreapp/sobre.html'), name='sobre'),
    path('filme/<int:filme_id>/', DetalheFilmeView.as_view(), name='detalhe_filme'),
    path('filmes_populares/', FilmesPopularesView.as_view(), name='filmes_populares')
]
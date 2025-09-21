from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('resultados/', TemplateView.as_view(template_name='coreapp/resultados.html'), name='resultados'),
    path('index/', TemplateView.as_view(template_name='coreapp/index.html'), name='index'),
]

from django.contrib import admin
from django.urls import path, include
from coreapp import views

urlpatterns = [
    path('', include('coreapp.urls')),
    path('admin/', admin.site.urls),
    path('ola/', views.ola),
    path('', views.ola),
]

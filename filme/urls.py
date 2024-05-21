from django.urls import path
from . import views

app_name = 'filme'

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('recomendacao/', views.recomendacao, name='recomendacao'),
    path('filme/', views.filme, name='filme'),
    path('categoria/', views.categoria, name='categoria'),
]

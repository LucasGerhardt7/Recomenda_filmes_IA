from django.urls import path
from . import views

app_name = 'filme'

urlpatterns = [
    path('', views.index, name='index'),
    path('filme/', views.filme, name='filme'),
    path('categoria/', views.categoria, name='categoria'),
]

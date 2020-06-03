from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='Raul-Home'),
    path('about/', views.secondHome, name='Raul-SecondHome'),

]
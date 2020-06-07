from django.urls import path
from . import views

urlpatterns = [
    path('', views.landingpage, name='Raul-landing'),
    path('raul-home/', views.home, name='Raul-Home'),
    path('home/', views.secondHome, name='Raul-SecondHome'),
    path('s/', views.search, name='search'),



]
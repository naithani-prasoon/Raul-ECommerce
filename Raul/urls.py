from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='Raul-Home'),
    path('home/', views.secondHome, name='Raul-SecondHome'),
    path('product/', views.products, name='Raul-product'),


]
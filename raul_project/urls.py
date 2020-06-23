"""raul_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path,include
from users import views as user_views
from raul_project import settings
from Raul import views
from carts import views as cart_views
from orders import views as orders
from Raul_Inc import views as Raul_Inc_Path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('category/<str:cats>/', views.CategoryView,name='cat-view'),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('profile/orders', user_views.profile, name='profile-orders'),
    path('product/', views.products, name='Raul-product'),
    path('product/<str:slug>/', views.singleView, name='Raul-single'),
    path('login/', auth_views.LoginView.as_view(template_name='Raul/Base.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),name='password_reset_complete'),
    path('', include('Raul.urls')),
    path('s/', views.search, name='search'),
    path('cart/<int:id>/', cart_views.remove_from_cart, name='remove_from_cart'),
    path('cart/<str:slug>/', cart_views.add_to_cart, name='add_to_cart'),
    path('checkout/', orders.checkout, name='checkout'),
    path('orders/', orders.orders, name='user_orders'),
    path('Raul_Inc/Home', Raul_Inc_Path.home, name='Raul_Inc_Home'),
    path('cart/', cart_views.view, name='cart'),
    path('ajax/add_user_address/',user_views.add_address, name='ajax_add_user_address'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

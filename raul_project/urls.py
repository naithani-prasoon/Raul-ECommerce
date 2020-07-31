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
    path('section/<str:sec>/', views.SectionView,name='sec-view'),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('venue/', user_views.venue, name='venue'),
    path('profile/orders', user_views.profile, name='profile-orders'),
    path('product/', views.products, name='Raul-product'),
    path('product/<str:slug>/', views.singleView, name='Raul-single'),
    path('login/', user_views.login_register, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'), name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),name='password_reset_complete'),
    path('', include('Raul.urls')),
    path('s/', views.search, name='search'),
    path('cart/<int:id>/', cart_views.remove_from_cart, name='remove_from_cart'),
    path('cart/<str:slug>/', cart_views.update_cart, name='update_cart'),
    path('cart/<str:slug>/', cart_views.add_to_cart, name='add_to_cart'),
    path('checkout/', orders.checkout, name='checkout'),
    path('orders/', orders.orders, name='user_orders'),
    path('Raul_Inc/Home', Raul_Inc_Path.home, name='Raul_Inc_Home'),
    path('Raul_Inc/bio', Raul_Inc_Path.bio, name='Raul_Inc_Bio'),
    path('Raul_Inc/press', Raul_Inc_Path.press, name='Raul_Inc_Press'),
    path('Raul_Inc/press-NYTimes.html', Raul_Inc_Path.NYTimes, name='Raul_Inc_NYTimes'),
    path('Raul_Inc/press-NY-Magazine.html', Raul_Inc_Path.NYMagazine, name='Raul_Inc_NY-Magazine'),
    path('Raul_Inc/press-coveteur.html', Raul_Inc_Path.presscoveteur, name='Raul_Inc_press-coveteur'),
    path('Raul_Inc/press-mtv.html', Raul_Inc_Path.pressmtv, name='Raul_Inc_press-mtv'),
    path('Raul_Inc/press-the-worlds-best-events.html', Raul_Inc_Path.presstheworldsbest, name='Raul_Inc_press-the-worlds-best-events'),
    path('Raul_Inc/presswwd.html', Raul_Inc_Path.presswwwd, name='Raul_Inc_presswwd'),
    path('Raul_Inc/press-met.html', Raul_Inc_Path.pressmet, name='Raul_Inc_press-met'),
    path('Raul_Inc/press-looktothestars.html', Raul_Inc_Path.presslooktothestars, name='Raul_Inc_press-looktothestars'),
    path('Raul_Inc/press-trendencias.html', Raul_Inc_Path.presstrendencias, name='Raul_Inc_press-trendencias'),
    path('Raul_Inc/press-ny-post.html', Raul_Inc_Path.pressnypost, name='Raul_Inc_press-ny-post'),
    path('Raul_Inc/press-pretaporter.html', Raul_Inc_Path.presspretaporter, name='Raul_Inc_press-pretaporter'),
    path('Raul_Inc/press-dailyfrontrow.html', Raul_Inc_Path.pressdaily, name='Raul_Inc_press-dailyfrontrow'),
    path('Raul_Inc/2019-pressvoguecom.html', Raul_Inc_Path.vougue, name='Raul_Inc_2019-pressvoguecom.html'),
    path('Raul_Inc/pressvogue.html', Raul_Inc_Path.vougue2, name='Raul_Inc_pressvogue.html'),
    path('Raul_Inc/cafe', Raul_Inc_Path.cafe, name='Raul_Inc_cafe'),
    path('Raul_Inc/press-jet-set.html', Raul_Inc_Path.pressjet, name='Raul_Inc_press-jet-set'),
    path('Raul_Inc/clientList', Raul_Inc_Path.clientList, name='Raul_Inc_clientList'),
    path('Raul_Inc/contact', Raul_Inc_Path.contact, name='Raul_Inc_contact'),
    path('Raul_Inc/gallery', Raul_Inc_Path.gallery, name='Raul_Inc_gallery'),
    path('cart/', cart_views.view, name='cart'),
    path('profile/<int:id>/', user_views.delete_address, name='del_add'),
    path('ajax/add_user_address/',user_views.add_address, name='ajax_add_user_address'),
    path('ajax/add_user_billing_address/',user_views.add_billing_address, name='ajax_add_user_billing_address'),
    path('ajax/add_to_cart/<str:slug>',orders.add_to_cart, name='ajax_add_to_cart'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

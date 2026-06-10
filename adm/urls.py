from django.urls import path
from django.shortcuts import redirect
from .views import *
from django.conf.urls.static import static
from django.conf import settings

def redirect_to_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    return redirect('login')

urlpatterns = [
    path('', redirect_to_login, name='root'),
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('home/',home, name='home'),
    path('seller/',seller , name='seller'),
    path('menu/',menu, name='menu'),
    path('about/',about, name='about'),
    path('cart/',cart, name='cart'),
    path('cart/remove/<int:cart_item_id>/', remove_cart_item, name='remove_cart_item'),
    path('cart/adjust/<int:cart_item_id>/', adjust_cart_quantity, name='adjust_cart_quantity'),
    path('checkout/', checkout, name='checkout'),
    path('orderSuccess/', orderSuccess, name='orderSuccess'),
    path('addToCart/<int:foodid>',addToCart, name='addToCart'),
    path('addFoodItem/', addFoodItem, name='addFoodItem'),
    path('edit/<item>/', editFoodItem, name='editFood'),
    path('delete/<item>/', deleteFoodItem, name='deleteFood'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

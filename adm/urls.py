from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', user_login, name='login'),
    path('home/',home, name='home'),
    path('seller/',seller , name='seller'),
    path('menu/',menu, name='menu'),
    path('about/',about, name='about'),
    path('cart/',cart, name='cart'),
    path('checkout/', checkout, name='checkout'),
    path('orderSuccess/', orderSuccess, name='orderSuccess'),
    path('addToCart/<int:foodid>',addToCart, name='addToCart'),
    path('addFoodItem/', addFoodItem, name='addFoodItem'),
    path('edit/<item>/', editFoodItem, name='editFood'),
    path('delete/<item>/', deleteFoodItem, name='deleteFood'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

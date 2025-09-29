from django.urls import path
from . import views

app_name = 'shopping_cart'

urlpatterns = [
    path('', views.CartDetailView.as_view(), name='cart_detail'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update/<int:product_id>/', views.update_cart_item, name='update_cart_item'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear/', views.clear_cart, name='clear_cart'),
]
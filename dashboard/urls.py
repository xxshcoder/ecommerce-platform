from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    # Dashboard home
    path('', views.dashboard_home, name='home'),
    
    # Products
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_add, name='product_add'),
    path('products/<int:product_id>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:product_id>/delete/', views.product_delete, name='product_delete'),
    path('products/image/<int:image_id>/delete/', views.delete_product_image, name='delete_product_image'),
    
    # Orders
    path('orders/', views.order_list, name='order_list'),
    path('orders/<str:order_number>/', views.order_detail, name='order_detail'),
    
    # Users
    path('users/', views.user_list, name='user_list'),
]
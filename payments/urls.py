from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('esewa/success/', views.esewa_payment_success, name='esewa_success'),
    path('esewa/failure/', views.esewa_payment_failure, name='esewa_failure'),
    path('order/<str:order_number>/esewa/', views.initiate_esewa_payment, name='initiate_esewa_payment'),
    path('order/<str:order_number>/cod/', views.cash_on_delivery, name='cash_on_delivery'),
    path('order/<str:order_number>/select/', views.payment_method_selection, name='payment_method_selection'),
]
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('category/<slug:slug>/', views.CategoryProductsView.as_view(), name='category_products'),
    path('brand/<slug:slug>/', views.BrandProductsView.as_view(), name='brand_products'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('search/', views.ProductSearchView.as_view(), name='product_search'),
    path('featured/', views.FeaturedProductsView.as_view(), name='featured_products'),
]
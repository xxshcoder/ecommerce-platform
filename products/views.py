from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from .models import Product, ProductCategory, Brand

class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        return Product.objects.filter(
            is_active=True,
            availability_status='in_stock'
        ).select_related('category', 'brand')

class CategoryProductsView(ListView):
    model = Product
    template_name = 'products/category_products.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        self.category = get_object_or_404(ProductCategory, slug=self.kwargs['slug'])
        return Product.objects.filter(
            category=self.category,
            is_active=True,
            availability_status='in_stock'
        ).select_related('category', 'brand')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

class BrandProductsView(ListView):
    model = Product
    template_name = 'products/brand_products.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        self.brand = get_object_or_404(Brand, slug=self.kwargs['slug'])
        return Product.objects.filter(
            brand=self.brand,
            is_active=True,
            availability_status='in_stock'
        ).select_related('category', 'brand')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brand'] = self.brand
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    
    def get_queryset(self):
        return Product.objects.filter(is_active=True).select_related('category', 'brand')

class ProductSearchView(ListView):
    model = Product
    template_name = 'products/search_results.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Product.objects.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query) |
                Q(sku__icontains=query),
                is_active=True,
                availability_status='in_stock'
            ).select_related('category', 'brand')
        return Product.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

class FeaturedProductsView(ListView):
    model = Product
    template_name = 'products/featured_products.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        return Product.objects.filter(
            is_featured=True,
            is_active=True,
            availability_status='in_stock'
        ).select_related('category', 'brand')
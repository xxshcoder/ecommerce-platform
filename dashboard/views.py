from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Sum, Count, F, Q
from django.utils import timezone
from datetime import timedelta
from django.core.paginator import Paginator
from django.http import JsonResponse

from products.models import Product, ProductCategory, Brand, ProductImage
from orders.models import Order, OrderItem
from users.models import UserProfile
from payments.models import Payment
from django.contrib.auth.models import User

# ------------------------------
# Dashboard Home
# ------------------------------
@staff_member_required
def dashboard_home(request):
    today = timezone.now().date()
    last_30_days = today - timedelta(days=30)
    last_7_days = today - timedelta(days=7)

    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    processing_orders = Order.objects.filter(status='processing').count()
    completed_orders = Order.objects.filter(status='delivered').count()

    recent_orders = Order.objects.all()[:5]

    total_revenue = Order.objects.filter(payment_status='completed').aggregate(total=Sum('total_amount'))['total'] or 0
    monthly_revenue = Order.objects.filter(payment_status='completed', created_at__gte=last_30_days).aggregate(total=Sum('total_amount'))['total'] or 0
    weekly_revenue = Order.objects.filter(payment_status='completed', created_at__gte=last_7_days).aggregate(total=Sum('total_amount'))['total'] or 0

    total_products = Product.objects.count()
    active_products = Product.objects.filter(is_active=True).count()
    low_stock_products = Product.objects.filter(track_quantity=True, quantity__lte=F('low_stock_threshold')).count()
    out_of_stock = Product.objects.filter(track_quantity=True, quantity=0).count()

    total_users = User.objects.count()
    new_users_month = User.objects.filter(date_joined__gte=last_30_days).count()

    top_products = Product.objects.annotate(total_sold=Count('orderitem')).order_by('-total_sold')[:5]

    context = {
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'processing_orders': processing_orders,
        'completed_orders': completed_orders,
        'recent_orders': recent_orders,
        'total_revenue': total_revenue,
        'monthly_revenue': monthly_revenue,
        'weekly_revenue': weekly_revenue,
        'total_products': total_products,
        'active_products': active_products,
        'low_stock_products': low_stock_products,
        'out_of_stock': out_of_stock,
        'total_users': total_users,
        'new_users_month': new_users_month,
        'top_products': top_products,
    }
    return render(request, 'dashboard/home.html', context)

# ------------------------------
# Product List
# ------------------------------
@staff_member_required
def product_list(request):
    products = Product.objects.select_related('category', 'brand').order_by('-created_at')

    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(sku__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )

    category_id = request.GET.get('category', '')
    if category_id:
        products = products.filter(category_id=category_id)

    status = request.GET.get('status', '')
    if status == 'active':
        products = products.filter(is_active=True)
    elif status == 'inactive':
        products = products.filter(is_active=False)
    elif status == 'low_stock':
        products = products.filter(track_quantity=True, quantity__lte=F('low_stock_threshold'))

    paginator = Paginator(products, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = ProductCategory.objects.all()
    context = {
        'products': page_obj,
        'categories': categories,
        'search_query': search_query,
    }
    return render(request, 'dashboard/products/list.html', context)

# ------------------------------
# Add Product
# ------------------------------
@staff_member_required
def product_add(request):
    if request.method == 'POST':
        try:
            product = Product.objects.create(
                name=request.POST.get('name'),
                sku=request.POST.get('sku'),
                category_id=request.POST.get('category'),
                brand_id=request.POST.get('brand') or None,
                description=request.POST.get('description'),
                short_description=request.POST.get('short_description', ''),
                price=request.POST.get('price'),
                compare_price=request.POST.get('compare_price') or None,
                quantity=request.POST.get('quantity', 0),
                track_quantity=request.POST.get('track_quantity') == 'on',
                is_active=request.POST.get('is_active') == 'on',
                is_featured=request.POST.get('is_featured') == 'on',
                featured_image=request.FILES.get('featured_image'),
            )

            for idx, image in enumerate(request.FILES.getlist('additional_images')):
                ProductImage.objects.create(product=product, image=image, sort_order=idx)

            messages.success(request, f'Product "{product.name}" added successfully!')
            return redirect('dashboard:product_list')

        except Exception as e:
            messages.error(request, f'Error adding product: {str(e)}')

    categories = ProductCategory.objects.all()
    brands = Brand.objects.all()
    return render(request, 'dashboard/products/add.html', {'categories': categories, 'brands': brands})

# ------------------------------
# Edit Product
# ------------------------------
@staff_member_required
def product_edit(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        try:
            product.name = request.POST.get('name')
            product.sku = request.POST.get('sku')
            product.category_id = request.POST.get('category')
            product.brand_id = request.POST.get('brand') or None
            product.description = request.POST.get('description')
            product.short_description = request.POST.get('short_description', '')
            product.price = request.POST.get('price')
            product.compare_price = request.POST.get('compare_price') or None
            product.quantity = request.POST.get('quantity', 0)
            product.track_quantity = request.POST.get('track_quantity') == 'on'
            product.is_active = request.POST.get('is_active') == 'on'
            product.is_featured = request.POST.get('is_featured') == 'on'

            if request.FILES.get('featured_image'):
                product.featured_image = request.FILES.get('featured_image')

            product.save()

            for idx, image in enumerate(request.FILES.getlist('additional_images')):
                ProductImage.objects.create(product=product, image=image, sort_order=product.images.count() + idx)

            messages.success(request, f'Product "{product.name}" updated successfully!')
            return redirect('dashboard:product_list')

        except Exception as e:
            messages.error(request, f'Error updating product: {str(e)}')

    categories = ProductCategory.objects.all()
    brands = Brand.objects.all()
    return render(request, 'dashboard/products/edit.html', {'product': product, 'categories': categories, 'brands': brands})

# ------------------------------
# Delete (Archive) Product
# ------------------------------
@staff_member_required
def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product.is_active = False  # Archive instead of delete
        product.save()
        messages.success(request, f'Product "{product.name}" has been archived.')
        return redirect('dashboard:product_list')

    return render(request, 'dashboard/products/delete_confirm.html', {'product': product})

# ------------------------------
# Delete Product Image
# ------------------------------
@staff_member_required
def delete_product_image(request, image_id):
    if request.method == 'POST':
        image = get_object_or_404(ProductImage, id=image_id)
        image.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})

# ------------------------------
# Orders
# ------------------------------
@staff_member_required
def order_list(request):
    orders = Order.objects.select_related('user').order_by('-created_at')

    status = request.GET.get('status', '')
    if status:
        orders = orders.filter(status=status)

    search_query = request.GET.get('search', '')
    if search_query:
        orders = orders.filter(
            Q(order_number__icontains=search_query) |
            Q(user__username__icontains=search_query) |
            Q(shipping_email__icontains=search_query)
        )

    paginator = Paginator(orders, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'dashboard/orders/list.html', {'orders': page_obj, 'search_query': search_query, 'status_filter': status})

@staff_member_required
def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status:
            order.status = new_status
            order.save()
            messages.success(request, f'Order status updated to {order.get_status_display()}')
            return redirect('dashboard:order_detail', order_number=order.order_number)

    return render(request, 'dashboard/orders/detail.html', {'order': order})

# ------------------------------
# Users
# ------------------------------
@staff_member_required
def user_list(request):
    users = User.objects.order_by('-date_joined')
    search_query = request.GET.get('search', '')
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )

    paginator = Paginator(users, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'dashboard/users/list.html', {'users': page_obj, 'search_query': search_query})

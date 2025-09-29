from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView
from .cart_manager import CartManager
from products.models import Product

class CartDetailView(TemplateView):
    template_name = 'shopping_cart/cart_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_manager = CartManager(self.request)
        cart_data = cart_manager.get_cart_data()
        context.update(cart_data)
        return context

@require_POST
def add_to_cart(request, product_id):
    """Add product to cart"""
    quantity = int(request.POST.get('quantity', 1))
    cart_manager = CartManager(request)
    success, message = cart_manager.add_item(product_id, quantity)
    
    # Check if it's an AJAX request
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if success:
            cart_data = cart_manager.get_cart_data()
            return JsonResponse({
                'success': True,
                'message': message,
                'cart_total_items': cart_data['total_items'],
                'cart_total': str(cart_data['total']),
            })
        return JsonResponse({'success': False, 'message': message})
    
    # Regular POST request - add message only once
    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)
    
    # Get the referer to redirect back
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('products:product_list')

@require_POST
def update_cart_item(request, product_id):
    """Update cart item quantity"""
    quantity = int(request.POST.get('quantity', 1))
    cart_manager = CartManager(request)
    success, message = cart_manager.update_item(product_id, quantity)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if success:
            cart_data = cart_manager.get_cart_data()
            # Get updated item
            item = next((item for item in cart_data['items'] if item.product.id == product_id), None)
            return JsonResponse({
                'success': True,
                'message': message,
                'item_total': str(item.total_price) if item else '0',
                'cart_subtotal': str(cart_data['subtotal']),
                'cart_tax': str(cart_data['tax']),
                'cart_total': str(cart_data['total']),
                'cart_total_items': cart_data['total_items'],
            })
        return JsonResponse({'success': False, 'message': message})
    
    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)
    
    return redirect('shopping_cart:cart_detail')

@require_POST
def remove_from_cart(request, product_id):
    """Remove item from cart"""
    cart_manager = CartManager(request)
    success, message = cart_manager.remove_item(product_id)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if success:
            cart_data = cart_manager.get_cart_data()
            return JsonResponse({
                'success': True,
                'message': message,
                'cart_subtotal': str(cart_data['subtotal']),
                'cart_tax': str(cart_data['tax']),
                'cart_total': str(cart_data['total']),
                'cart_total_items': cart_data['total_items'],
            })
        return JsonResponse({'success': False, 'message': message})
    
    if success:
        messages.success(request, message)
    else:
        messages.error(request, message)
    
    return redirect('shopping_cart:cart_detail')

@require_POST
def clear_cart(request):
    """Clear all items from cart"""
    cart_manager = CartManager(request)
    success, message = cart_manager.clear_cart()
    
    messages.success(request, message)
    return redirect('shopping_cart:cart_detail')
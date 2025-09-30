from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, DetailView
from django.utils.decorators import method_decorator
from django.db import transaction
from django.conf import settings
from .models import Order, OrderItem
from .forms import CheckoutForm
from shopping_cart.cart_manager import CartManager

@login_required
def checkout_view(request):
    """Checkout page"""
    cart_manager = CartManager(request)
    cart_data = cart_manager.get_cart_data()
    
    # Check if cart is empty
    if cart_data['total_items'] == 0:
        messages.warning(request, 'Your cart is empty. Please add items before checkout.')
        return redirect('shopping_cart:cart_detail')
    
    # Pre-fill form with user profile data if available
    initial_data = {}
    if hasattr(request.user, 'profile'):
        profile = request.user.profile
        initial_data = {
            'shipping_full_name': f"{request.user.first_name} {request.user.last_name}".strip(),
            'shipping_email': request.user.email,
            'shipping_phone': profile.phone_number,
            'shipping_address_line1': profile.address_line1,
            'shipping_address_line2': profile.address_line2,
            'shipping_city': profile.city,
            'shipping_state': profile.state,
            'shipping_postal_code': profile.postal_code,
            'shipping_country': profile.country,
            'payment_method': 'cod',  # Default to COD
        }
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    order = form.save(commit=False)
                    order.user = request.user
                    order.subtotal = cart_data['subtotal']
                    order.tax_amount = cart_data['tax']
                    order.shipping_cost = 0  # Free shipping
                    order.total_amount = cart_data['total']
                    order.save()
                    
                    # Create order items
                    for cart_item in cart_data['items']:
                        OrderItem.objects.create(
                            order=order,
                            product=cart_item.product,
                            product_name=cart_item.product.name,
                            product_sku=cart_item.product.sku,
                            product_price=cart_item.product.price,
                            quantity=cart_item.quantity
                        )
                        
                        # Update product stock
                        if cart_item.product.track_quantity:
                            cart_item.product.quantity -= cart_item.quantity
                            cart_item.product.save()
                    
                    # Clear cart
                    cart_manager.clear_cart()
                    
                    # Handle payment method
                    payment_method = form.cleaned_data['payment_method']
                    if payment_method == 'esewa':
                        # Redirect to payment initiation
                        return redirect('payments:initiate_esewa_payment', order_number=order.order_number)
                    else:
                        # Handle Cash on Delivery
                        return redirect('payments:cash_on_delivery', order_number=order.order_number)
                    
            except Exception as e:
                messages.error(request, f'Error placing order: {str(e)}')
                return redirect('orders:checkout')
    else:
        form = CheckoutForm(initial=initial_data)
    
    context = {
        'form': form,
        'cart': cart_data['cart'],
        'items': cart_data['items'],
        'subtotal': cart_data['subtotal'],
        'tax': cart_data['tax'],
        'total': cart_data['total'],
    }
    return render(request, 'orders/checkout.html', context)

@method_decorator(login_required, name='dispatch')
class OrderListView(ListView):
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    paginate_by = 10
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items')

@method_decorator(login_required, name='dispatch')
class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'
    slug_field = 'order_number'
    slug_url_kwarg = 'order_number'
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product')

@login_required
def cancel_order(request, order_number):
    """Cancel an order"""
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    
    if order.status in ['pending', 'processing']:
        with transaction.atomic():
            # Restore product stock
            for item in order.items.all():
                if item.product.track_quantity:
                    item.product.quantity += item.quantity
                    item.product.save()
            
            order.status = 'cancelled'
            order.payment_status = 'cancelled'
            order.save()
            messages.success(request, f'Order {order.order_number} has been cancelled.')
    else:
        messages.error(request, 'This order cannot be cancelled.')
    
    return redirect('orders:order_detail', order_number=order.order_number)
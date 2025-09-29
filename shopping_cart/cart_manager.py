from .models import Cart, CartItem
from products.models import Product
from django.shortcuts import get_object_or_404

class CartManager:
    def __init__(self, request):
        self.request = request
        self.cart = self._get_or_create_cart()

    def _get_or_create_cart(self):
        """Get or create cart based on user or session"""
        if self.request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=self.request.user)
        else:
            # For anonymous users, use session
            if not self.request.session.session_key:
                self.request.session.create()
            session_key = self.request.session.session_key
            cart, created = Cart.objects.get_or_create(session_key=session_key)
        return cart

    def add_item(self, product_id, quantity=1):
        """Add item to cart or update quantity if exists"""
        product = get_object_or_404(Product, id=product_id, is_active=True)
        
        try:
            # Check if item already exists
            cart_item = CartItem.objects.get(cart=self.cart, product=product)
            # Update existing item
            new_quantity = cart_item.quantity + quantity
            
            # Check stock availability
            if product.track_quantity and product.quantity < new_quantity:
                return False, f"Cannot add more items. Only {product.quantity} items available in stock."
            
            cart_item.quantity = new_quantity
            cart_item.save()
            return True, "Cart updated successfully"
            
        except CartItem.DoesNotExist:
            # Create new item
            # Check stock availability for new item
            if product.track_quantity and product.quantity < quantity:
                return False, "Insufficient stock available"
            
            CartItem.objects.create(
                cart=self.cart,
                product=product,
                quantity=quantity
            )
            return True, "Item added to cart successfully"

    def update_item(self, product_id, quantity):
        """Update item quantity in cart"""
        try:
            cart_item = CartItem.objects.get(cart=self.cart, product_id=product_id)
            product = cart_item.product

            if quantity <= 0:
                cart_item.delete()
                return True, "Item removed from cart"

            # Check stock
            if product.track_quantity and product.quantity < quantity:
                return False, f"Only {product.quantity} items available in stock"

            cart_item.quantity = quantity
            cart_item.save()
            return True, "Cart updated successfully"
        except CartItem.DoesNotExist:
            return False, "Item not found in cart"

    def remove_item(self, product_id):
        """Remove item from cart"""
        try:
            cart_item = CartItem.objects.get(cart=self.cart, product_id=product_id)
            cart_item.delete()
            return True, "Item removed from cart"
        except CartItem.DoesNotExist:
            return False, "Item not found in cart"

    def clear_cart(self):
        """Clear all items from cart"""
        self.cart.clear()
        return True, "Cart cleared successfully"

    def get_cart_data(self):
        """Get cart summary data"""
        items = self.cart.items.select_related('product').all()
        
        return {
            'cart': self.cart,
            'items': items,
            'total_items': self.cart.total_items,
            'subtotal': self.cart.subtotal,
            'tax': self.cart.tax_amount,
            'total': self.cart.total,
        }

    def merge_carts(self, user):
        """Merge session cart with user cart after login"""
        if not self.request.session.session_key:
            return

        try:
            session_cart = Cart.objects.get(session_key=self.request.session.session_key)
            user_cart, created = Cart.objects.get_or_create(user=user)

            # Merge items
            for session_item in session_cart.items.all():
                user_item, created = CartItem.objects.get_or_create(
                    cart=user_cart,
                    product=session_item.product,
                    defaults={'quantity': session_item.quantity}
                )
                if not created:
                    user_item.quantity += session_item.quantity
                    user_item.save()

            # Delete session cart
            session_cart.delete()
            self.cart = user_cart
        except Cart.DoesNotExist:
            pass
from .cart_manager import CartManager

def cart_context(request):
    """Add cart data to all templates"""
    try:
        cart_manager = CartManager(request)
        cart_data = cart_manager.get_cart_data()
        return {
            'cart_total_items': cart_data['total_items'],
            'cart_total': cart_data['total'],
        }
    except:
        return {
            'cart_total_items': 0,
            'cart_total': 0,
        }
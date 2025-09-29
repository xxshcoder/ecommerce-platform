from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from decimal import Decimal

class Cart(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='carts',
        null=True,
        blank=True
    )
    session_key = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        if self.user:
            return f"Cart - {self.user.username}"
        return f"Cart - Session {self.session_key}"

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def subtotal(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def tax_amount(self):
        # 10% tax rate - adjust as needed
        return self.subtotal * Decimal('0.10')

    @property
    def total(self):
        return self.subtotal + self.tax_amount

    def clear(self):
        self.items.all().delete()

class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, 
        on_delete=models.CASCADE, 
        related_name='items'
    )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-added_at']
        unique_together = ('cart', 'product')

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

    @property
    def total_price(self):
        return self.product.price * self.quantity

    @property
    def discount_amount(self):
        if self.product.is_on_sale:
            original_total = self.product.compare_price * self.quantity
            return original_total - self.total_price
        return Decimal('0.00')
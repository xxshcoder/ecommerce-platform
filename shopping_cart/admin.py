from django.contrib import admin
from .models import Cart, CartItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['total_price', 'added_at']
    fields = ['product', 'quantity', 'total_price', 'added_at']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'session_key', 'total_items', 'subtotal', 'created_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['user__username', 'session_key']
    readonly_fields = ['created_at', 'updated_at', 'total_items', 'subtotal', 'total']
    inlines = [CartItemInline]
    
    fieldsets = (
        ('Cart Information', {
            'fields': ('user', 'session_key')
        }),
        ('Summary', {
            'fields': ('total_items', 'subtotal', 'total')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity', 'total_price', 'added_at']
    list_filter = ['added_at', 'updated_at']
    search_fields = ['product__name', 'cart__user__username']
    readonly_fields = ['total_price', 'added_at', 'updated_at']
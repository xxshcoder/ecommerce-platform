from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'product_sku', 'product_price', 'quantity', 'total_price']
    can_delete = False
    
    def total_price(self, obj):
        return f"${obj.total_price}"
    total_price.short_description = 'Total'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_number', 'user', 'status', 'payment_status', 
        'total_amount', 'total_items', 'created_at'
    ]
    list_filter = ['status', 'payment_status', 'created_at']
    search_fields = ['order_number', 'user__username', 'user__email', 'shipping_email']
    readonly_fields = [
        'order_number', 'created_at', 'updated_at', 'total_items',
        'subtotal', 'tax_amount', 'total_amount'
    ]
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'status', 'payment_status')
        }),
        ('Shipping Information', {
            'fields': (
                'shipping_full_name', 'shipping_email', 'shipping_phone',
                'shipping_address_line1', 'shipping_address_line2',
                'shipping_city', 'shipping_state', 'shipping_postal_code', 'shipping_country'
            )
        }),
        ('Order Totals', {
            'fields': ('subtotal', 'tax_amount', 'shipping_cost', 'total_amount', 'total_items')
        }),
        ('Additional Information', {
            'fields': ('order_notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def total_items(self, obj):
        return obj.total_items
    total_items.short_description = 'Total Items'

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product_name', 'product_sku', 'product_price', 'quantity', 'item_total']
    list_filter = ['created_at']
    search_fields = ['order__order_number', 'product_name', 'product_sku']
    readonly_fields = ['product_name', 'product_sku', 'product_price', 'created_at', 'item_total']
    
    def item_total(self, obj):
        return f"${obj.total_price}"
    item_total.short_description = 'Item Total'
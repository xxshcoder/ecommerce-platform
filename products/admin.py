from django.contrib import admin
from django.utils.html import format_html
from .models import ProductCategory, Brand, Product, ProductImage

@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'product_count', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    
    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Products'

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'logo_preview', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="50" height="50" />', obj.logo.url)
        return "No logo"
    logo_preview.short_description = 'Logo'

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ['image', 'alt_text', 'is_primary', 'sort_order']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'sku', 'category', 'brand', 'price', 
        'quantity', 'availability_status', 'is_featured', 'created_at'
    ]
    list_filter = [
        'availability_status', 'is_active', 'is_featured', 
        'category', 'brand', 'created_at'
    ]
    search_fields = ['name', 'sku', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at', 'discount_info']
    inlines = [ProductImageInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'sku', 'category', 'brand')
        }),
        ('Description', {
            'fields': ('short_description', 'description')
        }),
        ('Pricing', {
            'fields': ('price', 'compare_price', 'cost_per_item', 'discount_info')
        }),
        ('Inventory', {
            'fields': ('track_quantity', 'quantity', 'low_stock_threshold')
        }),
        ('Status', {
            'fields': ('availability_status', 'is_active', 'is_featured')
        }),
        ('Media', {
            'fields': ('featured_image',)
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def discount_info(self, obj):
        if obj.is_on_sale:
            return format_html(
                '<span style="color: green;">{}% OFF</span>', 
                obj.discount_percentage
            )
        return "No discount"
    discount_info.short_description = 'Discount'

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image_preview', 'is_primary', 'sort_order']
    list_filter = ['is_primary', 'created_at']
    search_fields = ['product__name', 'alt_text']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" />', obj.image.url)
        return "No image"
    image_preview.short_description = 'Preview'
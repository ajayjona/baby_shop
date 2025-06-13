from django.contrib import admin
from .models import Category, Brand, Product, ProductImage, ProductVariant

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'alt_text', 'is_primary', 'order')

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ('size', 'color', 'style', 'price_adjustment', 'stock_quantity', 'sku', 'is_active')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'is_active', 'created_at')
    list_filter = ('is_active', 'parent')
    search_fields = ('name', 'description')
    fields = ('name', 'slug', 'description', 'parent', 'image', 'is_active')
    readonly_fields = ('slug', 'created_at', 'updated_at')

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    search_fields = ('name', 'description')
    fields = ('name', 'slug', 'description', 'logo', 'website', 'is_active')
    readonly_fields = ('slug', 'created_at', 'updated_at')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'vendor', 'category', 'brand', 'price', 'stock_quantity', 'is_active', 'is_featured')
    list_filter = ('category', 'brand', 'vendor', 'is_active', 'is_featured', 'age_range', 'condition')
    search_fields = ('name', 'description', 'short_description', 'tags')
    fieldsets = (
        (None, {'fields': ('name', 'slug', 'description', 'short_description')}),
        ('Details', {'fields': ('category', 'brand', 'vendor', 'price', 'original_price', 'stock_quantity', 'low_stock_threshold')}),
        ('Attributes', {'fields': ('age_range', 'condition', 'weight', 'dimensions')}),
        ('SEO', {'fields': ('meta_title', 'meta_description', 'tags')}),
        ('Status', {'fields': ('is_active', 'is_featured', 'is_digital')}),
        ('Ratings', {'fields': ('average_rating', 'total_reviews')}),
    )
    inlines = [ProductImageInline, ProductVariantInline]
    readonly_fields = ('slug', 'created_at', 'updated_at', 'average_rating', 'total_reviews')

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'is_primary', 'order', 'created_at')
    search_fields = ('product__name', 'alt_text')
    fields = ('product', 'image', 'alt_text', 'is_primary', 'order')

@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'color', 'style', 'stock_quantity', 'is_active')
    search_fields = ('product__name', 'sku')
    fields = ('product', 'size', 'color', 'style', 'price_adjustment', 'stock_quantity', 'sku', 'is_active')
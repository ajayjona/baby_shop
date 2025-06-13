from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem, Wishlist, WishlistItem

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1
    fields = ('product', 'variant', 'quantity')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1
    fields = ('product', 'variant', 'vendor', 'quantity', 'unit_price', 'subtotal', 'status')
    readonly_fields = ('unit_price', 'subtotal')

class WishlistItemInline(admin.TabularInline):
    model = WishlistItem
    extra = 1
    fields = ('product', 'added_at')
    readonly_fields = ('added_at',)

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('customer', 'total_items', 'total_price', 'created_at')
    search_fields = ('customer__username',)
    fields = ('customer',)
    inlines = [CartItemInline]
    readonly_fields = ('created_at', 'updated_at')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity', 'unit_price', 'subtotal')
    search_fields = ('cart__customer__username', 'product__name')
    fields = ('cart', 'product', 'variant', 'quantity')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'customer', 'status', 'payment_status', 'total_amount', 'created_at')
    list_filter = ('status', 'payment_status', 'created_at')
    search_fields = ('order_number', 'customer__username', 'shipping_email')
    fieldsets = (
        (None, {'fields': ('order_number', 'customer', 'status', 'payment_status')}),
        ('Pricing', {'fields': ('subtotal', 'shipping_cost', 'tax_amount', 'total_amount')}),
        ('Shipping', {'fields': ('shipping_name', 'shipping_email', 'shipping_phone', 'shipping_address_line_1', 'shipping_address_line_2', 'shipping_city', 'shipping_state', 'shipping_postal_code', 'shipping_country')}),
        ('Notes', {'fields': ('notes', 'special_instructions')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at', 'shipped_at', 'delivered_at'), 'classes': ('collapse',)}),
    )
    inlines = [OrderItemInline]
    readonly_fields = ('order_number', 'created_at', 'updated_at', 'total_amount')

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product_name', 'vendor', 'quantity', 'unit_price', 'subtotal', 'status')
    list_filter = ('status',)
    search_fields = ('order__order_number', 'product_name', 'vendor__username')
    fields = ('order', 'product', 'variant', 'vendor', 'product_name', 'product_description', 'unit_price', 'quantity', 'subtotal', 'status')
    readonly_fields = ('product_name', 'product_description', 'unit_price', 'subtotal')

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ('customer', 'created_at')
    search_fields = ('customer__username',)
    fields = ('customer',)
    inlines = [WishlistItemInline]
    readonly_fields = ('created_at', 'updated_at')

@admin.register(WishlistItem)
class WishlistItemAdmin(admin.ModelAdmin):
    list_display = ('wishlist', 'product', 'added_at')
    search_fields = ('wishlist__customer__username', 'product__name')
    fields = ('wishlist', 'product')
    readonly_fields = ('added_at',)
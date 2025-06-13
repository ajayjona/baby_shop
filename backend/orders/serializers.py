from rest_framework import serializers
from .models import Cart, CartItem, Order, OrderItem, Wishlist, WishlistItem
from products.serializers import ProductSerializer, ProductVariantSerializer
from users.serializers import UserSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    variant = ProductVariantSerializer(read_only=True)
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    class Meta:
        model = CartItem
        fields = ('id', 'cart', 'product', 'variant', 'quantity', 'unit_price', 'subtotal', 'created_at')
        read_only_fields = ('created_at', 'updated_at')

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.IntegerField(read_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    class Meta:
        model = Cart
        fields = ('id', 'customer', 'items', 'total_items', 'total_price', 'created_at')
        read_only_fields = ('created_at', 'updated_at')

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    variant = ProductVariantSerializer(read_only=True)
    vendor = UserSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = (
            'id', 'order', 'product', 'variant', 'vendor', 'product_name',
            'product_description', 'unit_price', 'quantity', 'subtotal', 'status', 'created_at'
        )
        read_only_fields = ('product_name', 'product_description', 'unit_price', 'subtotal', 'created_at')

class OrderSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    full_shipping_address = serializers.CharField(read_only=True)
    class Meta:
        model = Order
        fields = (
            'id', 'order_number', 'customer', 'status', 'payment_status', 'subtotal',
            'shipping_cost', 'tax_amount', 'total_amount', 'shipping_name', 'shipping_email',
            'shipping_phone', 'shipping_address_line_1', 'shipping_address_line_2', 'shipping_city',
            'shipping_state', 'shipping_postal_code', 'shipping_country', 'full_shipping_address',
            'notes', 'special_instructions', 'items', 'created_at'
        )
        read_only_fields = ('order_number', 'created_at', 'updated_at', 'total_amount')

class WishlistItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    class Meta:
        model = WishlistItem
        fields = ('id', 'wishlist', 'product', 'added_at')
        read_only_fields = ('added_at',)

class WishlistSerializer(serializers.ModelSerializer):
    items = WishlistItemSerializer(many=True, read_only=True)
    class Meta:
        model = Wishlist
        fields = ('id', 'customer', 'items', 'created_at')
        read_only_fields = ('created_at', 'updated_at')
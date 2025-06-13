# backend/orders/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
import uuid

User = get_user_model()

class Cart(models.Model):
    """Shopping cart for customers"""
    
    customer = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Cart for {self.customer.username}"
    
    @property
    def total_items(self):
        """Total number of items in cart"""
        return sum(item.quantity for item in self.items.all())
    
    @property
    def total_price(self):
        """Total price of all items in cart"""
        return sum(item.subtotal for item in self.items.all())

class CartItem(models.Model):
    """Individual items in shopping cart"""
    
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE
    )
    variant = models.ForeignKey(
        'products.ProductVariant',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    quantity = models.PositiveIntegerField(
        default=1,
        validators=[MinValueValidator(1)]
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.quantity}x {self.product.name}"
    
    @property
    def unit_price(self):
        """Price per unit (considering variant)"""
        if self.variant:
            return self.variant.final_price
        return self.product.price
    
    @property
    def subtotal(self):
        """Total price for this cart item"""
        return self.unit_price * self.quantity
    
    class Meta:
        unique_together = ['cart', 'product', 'variant']

class Order(models.Model):
    """Customer orders"""
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    # Order Identification
    order_number = models.CharField(max_length=20, unique=True, blank=True)
    
    # Customer Information
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    
    # Order Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending'
    )
    
    # Pricing
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    shipping_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)]
    )
    tax_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)]
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    
    # Shipping Information
    shipping_name = models.CharField(max_length=255)
    shipping_email = models.EmailField()
    shipping_phone = models.CharField(max_length=17)
    shipping_address_line_1 = models.CharField(max_length=255)
    shipping_address_line_2 = models.CharField(max_length=255, blank=True)
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    shipping_postal_code = models.CharField(max_length=20)
    shipping_country = models.CharField(max_length=100, default='Uganda')
    
    # Special Instructions
    notes = models.TextField(blank=True)
    special_instructions = models.TextField(blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = self.generate_order_number()
        super().save(*args, **kwargs)
    
    def generate_order_number(self):
        """Generate unique order number"""
        import random
        import string
        return 'BS' + ''.join(random.choices(string.digits, k=8))
    
    def __str__(self):
        return f"Order {self.order_number} - {self.customer.username}"
    
    @property
    def full_shipping_address(self):
        """Returns formatted shipping address"""
        address_parts = [
            self.shipping_address_line_1,
            self.shipping_address_line_2,
            self.shipping_city,
            self.shipping_state,
            self.shipping_postal_code,
            self.shipping_country
        ]
        return ', '.join([part for part in address_parts if part])
    
    class Meta:
        ordering = ['-created_at']

class OrderItem(models.Model):
    """Individual items in an order"""
    
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE
    )
    variant = models.ForeignKey(
        'products.ProductVariant',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    vendor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='order_items'
    )
    
    # Item Details (stored to preserve order history)
    product_name = models.CharField(max_length=255)
    product_description = models.TextField(blank=True)
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    
    # Variant details (if applicable)
    variant_details = models.JSONField(default=dict, blank=True)
    
    # Item Status
    status = models.CharField(
        max_length=20,
        choices=Order.STATUS_CHOICES,
        default='pending'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.quantity}x {self.product_name} (Order: {self.order.order_number})"
    
    def save(self, *args, **kwargs):
        # Auto-populate fields from product
        if not self.product_name:
            self.product_name = self.product.name
        if not self.product_description:
            self.product_description = self.product.short_description
        if not self.unit_price:
            self.unit_price = self.variant.final_price if self.variant else self.product.price
        if not self.subtotal:
            self.subtotal = self.unit_price * self.quantity
        if not self.vendor_id:
            self.vendor = self.product.vendor
            
        super().save(*args, **kwargs)

class Wishlist(models.Model):
    """Customer wishlist"""
    
    customer = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='wishlist'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Wishlist for {self.customer.username}"

class WishlistItem(models.Model):
    """Items in customer wishlist"""
    
    wishlist = models.ForeignKey(
        Wishlist,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE
    )
    added_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.product.name} in {self.wishlist.customer.username}'s wishlist"
    
    class Meta:
        unique_together = ['wishlist', 'product']
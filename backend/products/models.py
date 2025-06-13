# backend/products/models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify

User = get_user_model()

class Category(models.Model):
    """Product categories for baby/maternity products"""
    
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    
    # Category hierarchy
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories'
    )
    
    # Category image
    image = models.ImageField(
        upload_to='categories/',
        null=True,
        blank=True
    )
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

class Brand(models.Model):
    """Product brands"""
    
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(
        upload_to='brands/',
        null=True,
        blank=True
    )
    website = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

class Product(models.Model):
    """Main product model for baby/maternity items"""
    
    AGE_RANGE_CHOICES = [
        ('newborn', '0-3 months (Newborn)'),
        ('infant', '3-12 months (Infant)'),
        ('toddler', '1-3 years (Toddler)'),
        ('preschool', '3-5 years (Preschool)'),
        ('maternity', 'Maternity'),
        ('all_ages', 'All Ages'),
    ]
    
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('like_new', 'Like New'),
        ('good', 'Good'),
        ('fair', 'Fair'),
    ]
    
    # Basic Information
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField()
    short_description = models.CharField(max_length=500, blank=True)
    
    # Product Details
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )
    
    # Vendor Information
    vendor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products',
        limit_choices_to={'user_type': 'vendor'}
    )
    
    # Pricing
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    original_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0.01)]
    )
    
    # Inventory
    stock_quantity = models.PositiveIntegerField(default=0)
    low_stock_threshold = models.PositiveIntegerField(default=10)
    
    # Product Attributes
    age_range = models.CharField(
        max_length=20,
        choices=AGE_RANGE_CHOICES,
        default='all_ages'
    )
    condition = models.CharField(
        max_length=20,
        choices=CONDITION_CHOICES,
        default='new'
    )
    
    # Physical Properties
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Weight in kg"
    )
    dimensions = models.CharField(
        max_length=100,
        blank=True,
        help_text="L x W x H in cm"
    )
    
    # SEO and Marketing
    meta_title = models.CharField(max_length=60, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    tags = models.CharField(
        max_length=500,
        blank=True,
        help_text="Comma-separated tags"
    )
    
    # Status and Visibility
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_digital = models.BooleanField(default=False)
    
    # Ratings and Reviews
    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.00
    )
    total_reviews = models.PositiveIntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    @property
    def is_on_sale(self):
        """Check if product is on sale"""
        return self.original_price and self.price < self.original_price
    
    @property
    def discount_percentage(self):
        """Calculate discount percentage"""
        if self.is_on_sale:
            return round(((self.original_price - self.price) / self.original_price) * 100)
        return 0
    
    @property
    def is_in_stock(self):
        """Check if product is in stock"""
        return self.stock_quantity > 0
    
    @property
    def is_low_stock(self):
        """Check if product is low in stock"""
        return 0 < self.stock_quantity <= self.low_stock_threshold
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['vendor', 'is_active']),
            models.Index(fields=['price']),
            models.Index(fields=['created_at']),
        ]

class ProductImage(models.Model):
    """Product images"""
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Image for {self.product.name}"
    
    class Meta:
        ordering = ['order', 'created_at']

class ProductVariant(models.Model):
    """Product variants (size, color, etc.)"""
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='variants'
    )
    
    # Variant attributes
    size = models.CharField(max_length=50, blank=True)
    color = models.CharField(max_length=50, blank=True)
    style = models.CharField(max_length=100, blank=True)
    
    # Pricing and inventory for variant
    price_adjustment = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00
    )
    stock_quantity = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=100, unique=True, blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        variant_info = []
        if self.size:
            variant_info.append(f"Size: {self.size}")
        if self.color:
            variant_info.append(f"Color: {self.color}")
        if self.style:
            variant_info.append(f"Style: {self.style}")
        
        return f"{self.product.name} - {', '.join(variant_info)}"
    
    @property
    def final_price(self):
        """Calculate final price with adjustment"""
        return self.product.price + self.price_adjustment
    
    class Meta:
        unique_together = ['product', 'size', 'color', 'style']
from rest_framework import serializers
from .models import Category, Brand, Product, ProductImage, ProductVariant

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'description', 'parent', 'image', 'is_active', 'created_at')
        read_only_fields = ('slug', 'created_at', 'updated_at')

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('id', 'name', 'slug', 'description', 'logo', 'website', 'is_active', 'created_at')
        read_only_fields = ('slug', 'created_at', 'updated_at')

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'product', 'image', 'alt_text', 'is_primary', 'order', 'created_at')
        read_only_fields = ('created_at',)

class ProductVariantSerializer(serializers.ModelSerializer):
    final_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    class Meta:
        model = ProductVariant
        fields = ('id', 'product', 'size', 'color', 'style', 'price_adjustment', 'stock_quantity', 'sku', 'is_active', 'final_price', 'created_at')
        read_only_fields = ('created_at',)

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    is_on_sale = serializers.BooleanField(read_only=True)
    discount_percentage = serializers.IntegerField(read_only=True)
    is_low_stock = serializers.BooleanField(read_only=True)
    class Meta:
        model = Product
        fields = (
            'id', 'name', 'slug', 'description', 'short_description', 'category', 'brand',
            'vendor', 'price', 'original_price', 'stock_quantity', 'low_stock_threshold',
            'age_range', 'condition', 'weight', 'dimensions', 'meta_title', 'meta_description',
            'tags', 'is_active', 'is_featured', 'is_digital', 'average_rating', 'total_reviews',
            'is_on_sale', 'discount_percentage', 'is_low_stock', 'images', 'variants', 'created_at'
        )
        read_only_fields = ('slug', 'created_at', 'updated_at', 'average_rating', 'total_reviews')
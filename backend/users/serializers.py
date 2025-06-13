from rest_framework import serializers
from .models import User, VendorProfile

class UserSerializer(serializers.ModelSerializer):
    full_address = serializers.CharField(read_only=True)
    class Meta:
        model = User
        fields = (
            'id', 'username', 'email', 'user_type', 'phone_number', 'date_of_birth',
            'profile_picture', 'address_line_1', 'address_line_2', 'city', 'state',
            'postal_code', 'country', 'full_address', 'is_verified', 'is_active', 'created_at'
        )
        read_only_fields = ('created_at', 'updated_at', 'is_verified')

class VendorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = VendorProfile
        fields = (
            'id', 'user', 'business_name', 'business_description', 'business_license',
            'tax_id', 'business_phone', 'business_email', 'website', 'business_address',
            'is_verified', 'average_rating', 'total_reviews', 'created_at'
        )
        read_only_fields = ('created_at', 'updated_at', 'average_rating', 'total_reviews')
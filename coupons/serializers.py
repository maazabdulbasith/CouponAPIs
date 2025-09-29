# coupons/serializers.py
from rest_framework import serializers
from .models import Coupon
from decimal import Decimal

class CouponSerializer(serializers.ModelSerializer):
    is_valid = serializers.SerializerMethodField()

    class Meta:
        model = Coupon
        fields = ['id','code','discount_type','discount_value','expiry_date','usage_limit','used_count','active','min_cart_value','is_valid']

    def get_is_valid(self, obj):
        return obj.is_valid()

class ApplyCouponSerializer(serializers.Serializer):
    code = serializers.CharField()
    price = serializers.DecimalField(max_digits=12, decimal_places=2)

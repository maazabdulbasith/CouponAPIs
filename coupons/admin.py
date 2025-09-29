from django.contrib import admin
from .models import Coupon

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code','discount_type','discount_value','active','expiry_date','usage_limit','used_count')
    search_fields = ('code',)
    list_filter = ('active','discount_type')

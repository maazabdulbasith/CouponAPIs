from django.contrib import admin
from .models import Coupon
from django.contrib.auth.models import Group
from django.contrib.admin.sites import NotRegistered

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code','discount_type','discount_value','active','expiry_date','usage_limit','used_count')
    search_fields = ('code',)
    list_filter = ('active','discount_type')

# Hide Groups from admin sidebar
try:
    admin.site.unregister(Group)
except NotRegistered:
    pass

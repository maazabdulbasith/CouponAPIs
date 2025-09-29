from django.urls import path
from .views import CouponListView, ApplyCouponView, PreviewCouponView

urlpatterns = [
	path('coupons/', CouponListView.as_view(), name='coupon-list'),
	path('apply/', ApplyCouponView.as_view(), name='apply-coupon'),
	path('preview/', PreviewCouponView.as_view(), name='preview-coupon'),
]

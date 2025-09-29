from decimal import Decimal
from django.db import transaction
from django.db.models import F
from django.utils import timezone
from .models import Coupon
from .exceptions import (
	CouponNotFoundError,
	CouponInactiveError,
	CouponExpiredError,
	CouponMinCartValueError,
	CouponUsageLimitReachedError,
)


def _get_coupon_by_code_or_error(code: str) -> Coupon:
	try:
		return Coupon.objects.get(code=code)
	except Coupon.DoesNotExist:
		raise CouponNotFoundError("Invalid coupon code")


def _validate_coupon_for_price(coupon: Coupon, price: Decimal) -> None:
	if coupon.min_cart_value and price < coupon.min_cart_value:
		raise CouponMinCartValueError(
			f"Minimum cart value {coupon.min_cart_value} not met"
		)
	if coupon.is_expired():
		raise CouponExpiredError("Coupon expired")
	if not coupon.active:
		raise CouponInactiveError("Coupon inactive")


def preview_coupon(code: str, price: Decimal) -> dict:
	"""Non-mutating calculation to preview discount and final price."""
	normalized_code = code.strip().upper()
	coupon = _get_coupon_by_code_or_error(normalized_code)
	_validate_coupon_for_price(coupon, price)
	discount_amount, final_price = coupon.apply(price)
	return {
		"original_price": str(price),
		"discount_amount": str(discount_amount.quantize(Decimal("0.01"))),
		"final_price": str(final_price.quantize(Decimal("0.01"))),
		"coupon_code": coupon.code,
		"used_count": coupon.used_count,
	}


def redeem_coupon(code: str, price: Decimal) -> dict:
	"""Redeem a coupon once: validates and increments usage atomically."""
	normalized_code = code.strip().upper()
	coupon = _get_coupon_by_code_or_error(normalized_code)
	# Validate non-mutating rules first
	_validate_coupon_for_price(coupon, price)
	# Atomic usage increment with optimistic check
	with transaction.atomic():
		updated = Coupon.objects.filter(
			pk=coupon.pk,
			used_count__lt=F("usage_limit"),
		).update(used_count=F("used_count") + 1)
		if not updated:
			raise CouponUsageLimitReachedError("Usage limit reached")
		coupon.refresh_from_db()
		discount_amount, final_price = coupon.apply(price)
	return {
		"original_price": str(price),
		"discount_amount": str(discount_amount.quantize(Decimal("0.01"))),
		"final_price": str(final_price.quantize(Decimal("0.01"))),
		"coupon_code": coupon.code,
		"used_count": coupon.used_count,
	} 
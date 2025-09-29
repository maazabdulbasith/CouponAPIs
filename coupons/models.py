# coupons/models.py
from django.db import models
from django.utils import timezone
from decimal import Decimal

class Coupon(models.Model):
    FLAT = 'flat'
    PERCENT = 'percent'
    DISCOUNT_CHOICES = [(FLAT, 'Flat'), (PERCENT, 'Percentage')]

    code = models.CharField(max_length=50, unique=True, db_index=True)
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_CHOICES)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateTimeField()
    usage_limit = models.PositiveIntegerField(default=1, help_text='Global usage limit')
    used_count = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    min_cart_value = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_expired(self):
        return timezone.now() >= self.expiry_date

    def is_valid(self):
        return self.active and not self.is_expired() and (self.used_count < self.usage_limit)

    def calculate_discount_amount(self, price: Decimal) -> Decimal:
        if self.discount_type == self.FLAT:
            return min(self.discount_value, price)
        # percent
        return (price * self.discount_value / Decimal('100')).quantize(Decimal('0.01'))

    def apply(self, price: Decimal):
        """Return (discount_amount, final_price) without mutating DB."""
        discount = self.calculate_discount_amount(price)
        final_price = max(Decimal('0.00'), price - discount)
        return discount, final_price

    def __str__(self):
        return self.code

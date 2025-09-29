from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Coupon
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta

class ApplyCouponTests(APITestCase):
    def setUp(self):
        self.coupon = Coupon.objects.create(
            code='SAVE10',
            discount_type='percent',
            discount_value=Decimal('10'),
            expiry_date=timezone.now() + timedelta(days=1),
            usage_limit=2,
            active=True
        )

    def test_apply_success(self):
        resp = self.client.post(reverse('apply-coupon'), {'code':'SAVE10','price':'200.00'}, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data['final_price'], '180.00')

    def test_expired_coupon(self):
        self.coupon.expiry_date = timezone.now() - timedelta(days=1)
        self.coupon.save()
        resp = self.client.post(reverse('apply-coupon'), {'code':'SAVE10','price':'200.00'}, format='json')
        self.assertEqual(resp.status_code, 400)

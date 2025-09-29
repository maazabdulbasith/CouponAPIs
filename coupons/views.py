# coupons/views.py
from decimal import Decimal
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Coupon
from .serializers import CouponSerializer, ApplyCouponSerializer
from . import services
from .exceptions import (
	CouponNotFoundError,
	CouponInactiveError,
	CouponExpiredError,
	CouponMinCartValueError,
	CouponUsageLimitReachedError,
)


class CouponList(APIView):
	def get(self, request):
		coupons = Coupon.objects.all()
		serializer = CouponSerializer(coupons, many=True)
		return Response(serializer.data)


class PreviewCouponView(APIView):
	def post(self, request):
		serializer = ApplyCouponSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		code = serializer.validated_data['code']
		price = serializer.validated_data['price']
		try:
			data = services.preview_coupon(code, price)
			return Response(data, status=status.HTTP_200_OK)
		except CouponNotFoundError as e:
			return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
		except (CouponInactiveError, CouponExpiredError, CouponMinCartValueError) as e:
			return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ApplyCouponView(APIView):
	def post(self, request):
		serializer = ApplyCouponSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		code = serializer.validated_data['code']
		price = serializer.validated_data['price']
		try:
			data = services.redeem_coupon(code, price)
			return Response(data, status=status.HTTP_200_OK)
		except CouponNotFoundError as e:
			return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
		except CouponUsageLimitReachedError as e:
			return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
		except (CouponInactiveError, CouponExpiredError, CouponMinCartValueError) as e:
			return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

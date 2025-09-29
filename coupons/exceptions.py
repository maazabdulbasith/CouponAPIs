class CouponDomainError(Exception):
	pass


class CouponNotFoundError(CouponDomainError):
	pass


class CouponInactiveError(CouponDomainError):
	pass


class CouponExpiredError(CouponDomainError):
	pass


class CouponMinCartValueError(CouponDomainError):
	pass


class CouponUsageLimitReachedError(CouponDomainError):
	pass 
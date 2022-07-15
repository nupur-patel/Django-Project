from rest_framework.throttling import UserRateThrottle

class BurstPreventionThrottle(UserRateThrottle):
    scope = 'burst'
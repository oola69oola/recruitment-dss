from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed

class SafeJWTAuthentication(JWTAuthentication):
    """
    Safe JWT Authentication backend.
    If an expired or invalid token is supplied, returns None (anonymous user)
    rather than raising an unhandled AuthenticationFailed exception that blocks
    AllowAny endpoints. Secured endpoints with IsAuthenticated will still reject
    the anonymous user appropriately.
    """
    def authenticate(self, request):
        try:
            return super().authenticate(request)
        except (InvalidToken, AuthenticationFailed):
            return None


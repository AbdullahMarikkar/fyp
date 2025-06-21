from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from src.utils import jwtService

# Define paths that do not require authentication
PUBLIC_PATHS = [
    "/users/login",
    "/users/signup",
]


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """
        This middleware intercepts all incoming requests to check for a valid JWT.
        It bypasses checks for public paths. For protected paths, it verifies the
        token from the 'Authorization' header.
        """
        # Bypass authentication for public paths
        if request.url.path in PUBLIC_PATHS:
            response = await call_next(request)
            return response

        auth_header = request.headers.get("Authorization")

        # Check for the presence of the Authorization header
        if not auth_header:
            return Response("Not authenticated", status_code=401)

        # Check for correct 'Bearer' scheme
        try:
            scheme, token = auth_header.split()
            if scheme.lower() != "bearer":
                raise ValueError
        except ValueError:
            return Response("Invalid authorization scheme", status_code=401)

        # Verify the token
        try:
            user_payload = await jwtService.verify_token(token)
            # Attach the user payload to the request state for later use in dependencies
            request.state.user = user_payload
        except Exception as e:
            # This catches expired tokens, invalid signatures, etc.
            return Response(f"Invalid token: {str(e)}", status_code=401)

        response = await call_next(request)
        return response

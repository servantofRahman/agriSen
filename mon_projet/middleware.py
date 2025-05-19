import jwt
import logging
from django.conf import settings
from django.contrib.auth import get_user_model
from channels.middleware import BaseMiddleware
from urllib.parse import parse_qs
from channels.db import database_sync_to_async

User = get_user_model()

# Optional: Setup logger
logger = logging.getLogger(__name__)

class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        query_string = scope["query_string"].decode()
        query_params = parse_qs(query_string)
        token = query_params.get("token")

        if token:
            try:
                # Decode the JWT token
                payload = jwt.decode(token[0], settings.SECRET_KEY, algorithms=["HS256"])
                user = await self.get_user(payload["user_id"])

                if user:
                    # Attach the user to the WebSocket scope
                    scope["user"] = user
                else:
                    # If user does not exist, close connection
                    logger.warning(f"User with ID {payload['user_id']} not found.")
                    scope["user"] = None
                    await send({"type": "close"})

            except jwt.ExpiredSignatureError:
                # If the token has expired, handle the expiration case
                logger.warning("Token has expired.")
                scope["user"] = None
                await send({"type": "close"})

            except jwt.InvalidTokenError:
                # If the token is invalid
                logger.warning("Invalid token.")
                scope["user"] = None
                await send({"type": "close"})

        else:
            logger.warning("No token provided.")
            scope["user"] = None
            await send({"type": "close"})

        # Continue processing the WebSocket request
        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None


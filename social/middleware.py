from django.db import close_old_connections
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from jwt import decode as jwt_decode
from django.conf import settings
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
@database_sync_to_async
def get_user(validated_token):
    try:
        user = get_user_model().objects.get(id=validated_token["user_id"])
        return user
   
    except User.DoesNotExist:
        return AnonymousUser()

 
class TokenAuthMiddleware():
    def __init__(self, inner):
        self.inner = inner
    async def __call__(self, scope, receive, send, *args, **kwargs):
        close_old_connections()
        token = dict(scope)['path'].split("token=")[1]
        try:
            UntypedToken(token)
        except (InvalidToken, TokenError) as e:
            return None
        else:
            decoded_data = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = await get_user(decoded_data)
            
        return await self.inner(dict(scope, user=user), receive, send, *args, **kwargs)
from datetime import datetime

import pytz
from django.core.cache import cache
from rest_framework import HTTP_HEADER_ENCODING, exceptions
from rest_framework.authentication import BaseAuthentication
from rest_framework.authtoken.models import Token


def get_authorization_header(request):
    auth = request.META.get('HTTP_AUTHORIZATION', b'')
    if isinstance(auth, type('')):
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth


class ExpiringTokenAuthentication(BaseAuthentication):
    model = Token

    def authenticate(self, request):
        auth = get_authorization_header(request)

        if not auth:
            return None
        try:
            token = auth.decode()
        except UnicodeError:
            msg = 'Invalid token header. Token string should not contain invalid characters.'
            raise exceptions.AuthenticationFailed(msg)
        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        # 增加了缓存机制
        # 首先先从缓存中查找
        token_cache = 'token_' + key
        cache_user = cache.get(token_cache)
        if cache_user:
            return cache_user.user, cache_user  # 首先查看token是否在缓存中，若存在，直接返回用户
        try:
            token = self.model.objects.get(key=key[6:])

        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed('认证失败')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('用户被禁止')

        utc_now = datetime.datetime.utcnow()

        if (utc_now.replace(tzinfo=pytz.timezone("UTC")) - token.created.replace(
                tzinfo=pytz.timezone("UTC"))).days > 14:  # 设定存活时间 14天
            raise exceptions.AuthenticationFailed('认证信息过期')

        if token:
            token_cache = 'token_' + key
            cache.set(token_cache, token, 24 * 7 * 60 * 60)  # 添加 token_xxx 到缓存
        return token.user, token

    def authenticate_header(self, request):
        return 'Token'

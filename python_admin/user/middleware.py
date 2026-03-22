from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from jwt import ExpiredSignatureError, InvalidTokenError, PyJWTError
from rest_framework_jwt.settings import api_settings


class JwtAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 1. 扩大白名单检测
        path = request.path
        # 兼容 /user/login, /api/user/login, /media, /api/media 等各种路径
        if any(path.startswith(w) for w in ['/user/login', '/user/captcha', '/media', '/api/']):
            # 如果是媒体文件，直接放行
            if 'media' in path:
                return None

            # 如果是登录和验证码，直接放行
            if any(p in path for p in ['/login', '/captcha']):
                return None

        # 2. 进行 Token 验证
        token = request.META.get('HTTP_AUTHORIZATION')

        # 重点：先判断 token 是否存在
        if not token:
            return HttpResponse('未携带Token，请登录', status=401)

        try:
            # 如果 token 带有 "Bearer " 前缀，需要先处理掉（根据你前端发送格式定）
            # if token.startswith('Bearer '): token = token.split(' ')[1]

            jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
            jwt_payload = jwt_decode_handler(token)
            return None  # 验证通过

        except ExpiredSignatureError:
            return HttpResponse('Token过期，请重新登录', status=401)
        except (InvalidTokenError, PyJWTError):
            return HttpResponse('Token无效', status=401)

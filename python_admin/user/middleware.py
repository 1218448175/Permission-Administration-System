from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
from jwt import ExpiredSignatureError, InvalidTokenError, PyJWTError
from rest_framework_jwt.settings import api_settings


class JwtAuthenticationMiddleware(MiddlewareMixin):
    """
    自定义token鉴权中间件
    """

    def process_request(self, request):
        white_list = ['/user/login', '/user/captcha']  # 请求白名单
        path = request.path
        if path not in white_list and not path.startswith('/media'):
            print('要进行token验证')
            token = request.META.get('HTTP_AUTHORIZATION')
            try:
                jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
                jwt_payload = jwt_decode_handler(token)
            except ExpiredSignatureError:
                return HttpResponse('Token过期，请重新登录')
            except InvalidTokenError:
                return HttpResponse('Token无效')
            except PyJWTError:
                return HttpResponse('Token验证异常')
        else:
            print('无需验证')
            return None

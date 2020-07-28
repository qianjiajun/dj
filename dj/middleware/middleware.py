from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

from dj.utils.result import Result
from dj.utils.sql import ora
from dj.utils.token import Token


class RequiredMiddleware(MiddlewareMixin):

    def process_request(self, request):
        print(self, request.path)
        """产生request对象之后，url匹配之前调用
        :rtype: object
        """
        if request.path == '/login/' or request.path == '/logout/':
            pass
        else:
            access_token = request.META.get('HTTP_TOKEN')
            if access_token is None:
                return Result().fail("验证失败", "令牌为空", None)
            else:
                claims = Token.get_claims(access_token)
                if claims is None:
                    return Result().fail("验证失败", "非法令牌", None)
                password = ora().execute_value(
                    "SELECT password FROM auth.sys_password WHERE user_id='{id}'".format(id=claims['credit']))
                is_valid = Token(str(claims['credit']), password).certify_token(access_token)
                if is_valid:
                    pass
                else:
                    return Result().fail("验证失败", "令牌验证失败", None)


class ExceptionMiddleware(MiddlewareMixin):

    def process_exception(self, request, exception):
        print(self, request.path)
        print('Exception:', exception)
        return HttpResponse('500错误')

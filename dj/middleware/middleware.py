from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from dj.utils.exception import MyException
from dj.utils.result import Result
from dj.utils.sql import MsOracle
from dj.utils.token import Token

ora = MsOracle.ora()


class RequiredMiddleware(MiddlewareMixin):

    white_list = ['/login/', ]
    black_list = ['/black/', ]

    def process_request(self, request):
        print(self, request.path)
        """产生request对象之后，url匹配之前调用
        :rtype: object
        """
        if request.path in self.white_list:
            pass
        else:
            access_token = request.META.get('HTTP_TOKEN')
            if access_token is None:
                return JsonResponse(Result().fail("验证失败", "令牌为空", None).res)
            else:
                claims = Token.get_claims(access_token)
                if claims is None:
                    return JsonResponse(Result().fail("验证失败", "非法令牌", None).res)
                password = ora.execute_value(
                    "SELECT password FROM auth.sys_password WHERE user_id='{id}'".format(id=claims['credit']))
                is_valid = Token(str(claims['credit']), password).certify_token(access_token)
                if is_valid:
                    pass
                else:
                    return JsonResponse(Result().fail("验证失败", "令牌验证失败", None).res)
                    # return HttpResponse(Result().fail("验证失败", "令牌验证失败", None).to_string(),
                    # content_type=ContentType.JSON)

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        response = response or self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response


class ExceptionMiddleware(MiddlewareMixin):

    def process_exception(self, request, exception):
        print(self, request.path)
        if isinstance(exception, MyException):
            return JsonResponse(Result().fail(exception.get_message(), exception.get_detail(), None).res)
        else:
            return JsonResponse(Result().fail('操作失败', exception.args[0], None).res)

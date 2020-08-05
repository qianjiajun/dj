from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

from dj.utils.conn import ConnUtil
from dj.utils.exception import MyException
from dj.utils.result import Result
from dj.utils.token import Token

rc = ConnUtil.get_redis()
auth = ConnUtil.get_db("auth")
redis_set = ConnUtil.get_settings("REDIS_SET")
white_list = ConnUtil.get_settings("WHITE_LIST")
uncheck_list = ConnUtil.get_settings("UNCHECK_LIST")
black_list = ConnUtil.get_settings("BLACK_LIST")


class RequiredMiddleware(MiddlewareMixin):

    def process_request(self, request):
        print(self, request.path)
        """产生request对象之后，url匹配之前调用
        :rtype: object
        """
        if request.path in white_list:
            pass
        if request.path in black_list:
            return JsonResponse(Result().fail("验证失败", "非法接口, 已移入黑名单", None).res)
        else:
            access_token = request.META.get('HTTP_TOKEN')
            if access_token is None:
                return JsonResponse(Result().fail("验证失败", "令牌为空", None).res)
            else:
                claims = Token.get_claims(access_token)
                if claims is None:
                    return JsonResponse(Result().fail("验证失败", "非法令牌", None).res)
                password = auth.execute_value(
                    "SELECT password FROM auth.sys_password WHERE user_id='{id}'".format(id=claims['credit']))
                is_valid = Token(str(claims['credit']), password).certify_token(access_token)
                if is_valid:
                    if request.path in uncheck_list:
                        pass
                    else:
                        check_token = rc.get(str(claims['credit']))
                        if check_token is None:
                            return JsonResponse(Result().fail("验证失败", "令牌过期", None).is_login(False).res)
                        elif check_token == access_token:
                            rc.set_ex(access_token, claims['timestamp'], redis_set['expired'])
                            rc.set_ex(str(claims['credit']), access_token, redis_set['expired'])
                            pass
                        else:
                            return JsonResponse(Result().fail("验证失败", "令牌失效，已更新", None).is_login(False).res)
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

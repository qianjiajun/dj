from django.http import HttpResponse, HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin

from dj.utils.sql import MsOracle
from dj.utils.token import Token


class TestMiddleware(MiddlewareMixin):
    """中间件类"""

    def __init__(self):
        """服务器重启之后，接收第一个请求时调用(只会调用一次)"""
        print('----init----')

    # 中间件函数。(用到哪个函数写哪个，不需要全写)
    def process_request(self, request):
        """产生request对象之后，url匹配之前调用"""
        print(self, '----process_request----')
        # return HttpResponse('process_request') # 默认放行,不拦截请求。

    def process_view(self, request, view_func, *view_args, **view_kwargs):
        """url匹配之后，视图函数调用之前调用"""
        print(self, '----process_view----')
        # view_func: url匹配到的视图函数。
        return HttpResponse('process_view')  # return HttpResponse对象,表示拦截,直接执行process_response函数。

    def process_response(self, request, response):
        """视图函数调用之后，response返回浏览器之前"""
        print(self, '----process_response----')
        return response  # 一般会返回响应。


class RequiredMiddleware(MiddlewareMixin):

    # 中间件函数。(用到哪个函数写哪个，不需要全写)
    def process_request(self, request):
        """产生request对象之后，url匹配之前调用
        :rtype: object
        """
        if request.path == '/login/' or request.path == '/logout/':
            pass
        else:
            access_token = request.META.get('HTTP_TOKEN')
            if access_token is None:
                raise Exception('token为空')
            else:
                # ms_oracle().execute_object('select from ')
                claims = Token.get_claims(access_token)
                if claims is None:
                    pass
                # timestamp = claims['timestamp']
                # print('timestamp', timestamp)
                print(self, '----process_request----')
            # return HttpResponse('process_request') # 默认放行,不拦截请求。

    def __call__(self, request):
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        response = response or self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response


# 定义中间件类，处理全局异常
class ExceptionTestMiddleware(MiddlewareMixin):
    # 如果注册多个process_exception函数，那么函数的执行顺序与注册的顺序相反。(其他中间件函数与注册顺序一致)
    # 中间件函数，用到哪个就写哪个，不需要写所有的中间件函数。
    def process_exception(self, request, exception):
        """视图函数发生异常时调用"""
        print(self, '----process_exception1----')
        print(exception)

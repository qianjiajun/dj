from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from dj.utils.result import result
from dj.utils.cache import redis_cache
from dj.utils.sql import ms_oracle
from dj.utils.token import token

rc = redis_cache('123456')
ora = ms_oracle("auth", "auth", "115.239.175.246:3013/wxcz")


@require_http_methods(['GET', 'POST'])
def login(request):
    if request.method == 'GET':
        return render(request, "login.html")
    username = request.POST['username']
    sql = ["select ", "id \"id\"", ",username \"username\"", ",true_name \"trueName\" ",
           "from auth.sys_user ", "where username='{username}'".format(username=username)]
    user = ora.execute_object("".join(sql))
    if user is None:
        return HttpResponse(result().fail("登陆失败", "用户不存在").to_string())
    password = request.POST['password']
    sql = ["select password \"password\" from auth.sys_password ",
           "where password=fn_md5('{password}') and user_id='{id}'".format(password=password, id=user['id'])]
    password_obj = ora.execute_object("".join(sql))
    if password_obj is None:
        return HttpResponse(result().fail("登陆失败", "密码错误").to_string())
    token_obj = token(str(user['id']), password_obj['password']).generate_token()
    rc.set_ex(token_obj.token, token_obj.claims['timestamp'], 60)
    rs = result().set_message('登录成功').set_data(user).set_token(token_obj.token)
    # return render(request, "login.html", rs.res)
    return JsonResponse(rs.res)


@require_http_methods(['GET'])
def index(request):
    return render(request, "index.html")


def logout(request):
    rs = result().set_message('注销成功')
    rc.delete('token')
    return render(request, "login.html", rs.res)

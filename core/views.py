from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_http_methods

from dj.utils.conn import ConnUtil
from dj.utils.result import Result
from dj.utils.token import Token

rc = ConnUtil.get_redis()
auth = ConnUtil.get_db("auth")
redis_set = ConnUtil.get_settings("REDIS_SET")


@require_http_methods(['POST'])
def login(request):
    username = request.POST['username']
    sql = ["select ", "id \"id\"", ",username \"username\"", ",true_name \"trueName\" ",
           "from auth.sys_user ", "where username='{username}'".format(username=username)]
    user = auth.execute_object("".join(sql))
    if user is None:
        return HttpResponse(Result().fail("登陆失败", "用户不存在").to_string())
    password = request.POST['password']
    sql = ["select password \"password\" from auth.sys_password ",
           "where password=fn_md5('{password}') and user_id='{id}'".format(password=password, id=user['id'])]
    password_obj = auth.execute_object("".join(sql))
    if password_obj is None:
        return HttpResponse(Result().fail("登陆失败", "密码错误").to_string())
    token_obj = Token(str(user['id']), password_obj['password']).generate_token()
    old_token = rc.get(user['id'])
    rc.set_ex(token_obj.token, token_obj.claims['timestamp'], redis_set['expired'])
    rc.set_ex(user['id'], token_obj.token, redis_set['expired'])
    rc.delete(old_token)
    rs = Result().set_message('登录成功').set_data(user).set_token(token_obj.token)
    return JsonResponse(rs.res)


@require_http_methods(['POST'])
def logout(request):
    access_token = request.META['HTTP_TOKEN'];
    claims = Token.get_claims(access_token)
    if claims is not None:
        check_token = rc.get(claims['credit'])
        if access_token == check_token:
            rc.delete(claims['credit'])
    rc.delete(access_token)
    rs = Result().set_message('注销成功')
    return JsonResponse(rs.res)

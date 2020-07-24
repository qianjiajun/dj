from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from dj.utils.result import result
from dj.utils.sql import ms_oracle

ora = ms_oracle("auth", "auth", "115.239.175.246:3013/wxcz")


@require_http_methods(['GET', 'POST'])
def index(request):
    if request.method == 'GET':
        return render(request, "user/index.html")
    key = request.POST['key']
    sql = ["select ", "id \"id\"", ",username \"username\"", ",true_name \"trueName\" ",
           "from auth.sys_user ", "where username||true_name like '%{key}%' ".format(key=key),
           "order by id"]
    user_list, count = ora.execute_list("".join(sql))
    rs = result().set_message('读取数据成功').set_data(user_list).set_extra(count)
    return JsonResponse(rs.res)

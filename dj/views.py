from django.shortcuts import render

from dj.utils.sql import MsMysql, MsOracle

ms = MsMysql.ms()
ora = MsOracle.ora()


def mysql(request):
    ctx = {}
    if request.method == 'GET':
        if request.GET and request.GET['q']:
            ctx['message'] = request.GET['q']
        else:
            render(request, "sql/mysql.html")
    else:
        if request.POST['q']:
            sql = ["select ", "id_ \"id\"", ",account_ \"username\"", ",fullname_ \"trueName\" ",
                   "from org_user ", "where fullname_ like '%{trueName}%'".format(trueName=request.POST['q'])]
            data = ms.execute_list("".join(sql))
            ctx['message'] = request.POST['q']
            ctx['data'] = data
            print('mysql', data)
        else:
            ctx['message'] = "你提交了空表单"
    return render(request, "sql/mysql.html", ctx)


def oracle(request):
    ctx2 = {}
    if request.method == 'GET':
        if request.GET and request.GET['q']:
            ctx2['message'] = request.GET['q']
        else:
            render(request, "sql/oracle.html")
    else:
        if request.POST['q']:
            sql = ["select ", "id_ \"id\"", ",account_ \"username\"", ",fullname_ \"trueName\" ",
                   "from org_user ", "where fullname_ like '%{trueName}%'".format(trueName=request.POST['q'])]
            data = ora.execute_list("".join(sql))
            ctx2['message'] = request.POST['q']
            ctx2['data'] = data
            print('oracle', data)
        else:
            ctx2['message'] = "你提交了空表单"
    return render(request, "sql/oracle.html", ctx2)


def jump(request):
    page = request.GET['page']
    return render(request, page)


def page_not_found(request, exception):
    return render(request, 'error/404.html', {'error': '访问有误:页面不存在'}, status=404)


def server_error(request):
    return render(request, 'error/500.html', {'error': '访问有误:服务器错误'}, status=500)


def bad_request(request, exception):
    return render(request, 'error/400.html', {'error': exception}, status=400)

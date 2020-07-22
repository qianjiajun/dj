from django.http import HttpResponse

from dj.utils.result import resultSet


def login(request):
    rs = resultSet().set_message('登录成功').to_string()
    print(rs)
    return HttpResponse(rs)


def logout(request):
    rs = resultSet().set_message('注销成功').to_string()
    print(rs)
    return HttpResponse(rs)

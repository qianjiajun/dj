# -*- coding: utf-8 -*-

# 表单
from django.shortcuts import render


# 接收请求数据
def search(request):
    request.encoding = 'utf-8'
    ctx = {}
    if request.method == 'GET':
        if request.GET and request.GET['q']:
            ctx['message'] = request.GET['q']
        else:
            render(request, "login.html")
    else:
        if request.POST['q']:
            ctx['message'] = request.POST['q']
        else:
            ctx['message'] = "你提交了空表单"
    return render(request, "login.html", ctx)

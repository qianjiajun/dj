# -*- coding: utf-8 -*-

# 表单
from django.shortcuts import render
from dj.utils.sql import ms_mysql

ms = ms_mysql('localhost', "root", "root", "bpm", 3306)


def search(request):
    ctx = {}
    if request.method == 'GET':
        if request.GET and request.GET['q']:
            ctx['message'] = request.GET['q']
        else:
            render(request, "login.html")
    else:
        if request.POST['q']:
            data = ms.__execute_list__("select * from org_user where fullname_ like '%" + request.POST['q'] + "%'")
            ctx['message'] = request.POST['q']
            ctx['data'] = data
            print(data)
        else:
            ctx['message'] = "你提交了空表单"
    return render(request, "login.html", ctx)

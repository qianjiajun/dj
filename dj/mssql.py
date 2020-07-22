# -*- coding: utf-8 -*-

# 表单
from django.shortcuts import render
from dj.utils.sql import ms_mysql, ms_oracle

ms = ms_mysql('localhost', "root", "root", "bpm", 3306)
ora = ms_oracle("bpm", "bpm", "10.10.10.28:1521/WXCZ")


def mysql(request):
    ctx = {}
    if request.method == 'GET':
        if request.GET and request.GET['q']:
            ctx['message'] = request.GET['q']
        else:
            render(request, "mysql.html")
    else:
        if request.POST['q']:
            data = ms.execute_list("select * from org_user where fullname_ like '%" + request.POST['q'] + "%'")
            ctx['message'] = request.POST['q']
            ctx['data'] = data
            print('mysql', data)
        else:
            ctx['message'] = "你提交了空表单"
    return render(request, "mysql.html", ctx)


def oracle(request):
    ctx2 = {}
    if request.method == 'GET':
        if request.GET and request.GET['q']:
            ctx2['message'] = request.GET['q']
        else:
            render(request, "oracle.html")
    else:
        if request.POST['q']:
            data = ms.execute_list("select * from org_user where fullname_ like '%" + request.POST['q'] + "%'")
            ctx2['message'] = request.POST['q']
            ctx2['data'] = data
            print('oracle', data)
        else:
            ctx2['message'] = "你提交了空表单"
    return render(request, "oracle.html", ctx2)

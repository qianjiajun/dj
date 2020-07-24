from django.shortcuts import render

# settings.py debug=False


def jump(request):
    page = request.GET['page']
    return render(request, page)


def page_not_found(request, exception):
    return render(request, 'error/404.html', {'error': '访问有误:页面不存在'}, status=404)


def server_error(request):
    return render(request, 'error/500.html', {'error': '访问有误:服务器错误'}, status=500)


def bad_request(request, exception):
    return render(request, 'error/400.html', {'error': exception}, status=400)

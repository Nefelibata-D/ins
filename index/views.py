from django.shortcuts import render, redirect


def index(request):
    return render(request, 'index.html', locals())


# 404
def page_not_found(request, exception):
    return render(request, '404.html', locals())


# 500
def page_error(request):
    return render(request, '500.html')

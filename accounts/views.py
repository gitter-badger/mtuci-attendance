from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect

def login(request):
    next = request.GET.get('next', '/')
    if request.user.is_authenticated():
        return HttpResponseRedirect(next)
    if request.method == "GET":
        return render(request,
                      'accounts/login.html',
                      {'next': next, 'err': request.GET.get('err', '0')})
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(next)
        else:
            return HttpResponseRedirect('/login/?next='+next+'&err=1')

def logout(request):
    next = request.GET.get('next', '/')
    if request.user.is_authenticated():
        auth.logout(request)
        return HttpResponseRedirect(next)
    else:
        return HttpResponseRedirect(next)

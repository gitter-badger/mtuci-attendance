import re
from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from accounts.models import Account
from django.core import serializers

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

def getSearchArray(query):
    splitSymbols = re.compile(r'\b[.,:;\s]+\b')
    notNeedSymbols = re.compile(r'[^a-zA-Zа-яА-ЯёЁ0-9]+')
    return [notNeedSymbols.sub('', word).lower() for word in splitSymbols.split(query)]

def getSearchForUsers(queryArray):
    users = []
    for word in queryArray:
        for userDict in Account.objects.filter(Q(username__icontains=word) | \
                                               Q(first_name__icontains=word) | \
                                               Q(last_name__icontains=word) | \
                                               Q(patronymic__icontains=word)).values('id',
                                                                                     'first_name',
                                                                                     'last_name',
                                                                                     'patronymic',
                                                                                     'universityGroup__name'):
            users.append(userDict)
    return users

def getAllUsers():
    usersQS = Account.objects.all().values('id',
                                           'first_name',
                                           'last_name',
                                           'patronymic',
                                           'universityGroup__name')
    users = []
    for userDict in usersQS:
        users.append(userDict)
    return users

@login_required
def searchAccounts(request):
    if not request.is_ajax():
        raise PermissionDenied
    # Проверка прав
    if (not request.user.is_admin and not request.user.is_deanery) or \
        not request.user.is_active:
        raise PermissionDenied
    target = request.GET.get('target', 'all')
    q = request.GET.get('q', '')
    if target == 'user':
        if not q:
            return HttpResponseBadRequest()
        return JsonResponse(getSearchForUsers(getSearchArray(q)), safe=False)
    if target == 'all_users':
        return JsonResponse(getAllUsers(), safe=False)
    elif target == 'group':
        pass
    elif target == 'all':
        pass
    else:
        return HttpResponseBadRequest()

@login_required
def userInfo(request):
    if not request.is_ajax():
        raise PermissionDenied
    # Проверка прав
    id = request.GET.get('id')
    if not id:
        return HttpResponseBadRequest()
    try:
        user = Account.objects.get(id=id)
    except Account.DoesNotExist:
        return HttpResponseBadRequest()
    if  not request.user.is_active or \
        (not request.user.is_admin and \
        not request.user.is_deanery and \
        request.user.id != id and not \
        request.user.is_steward and \
        request.user.universityGroup != user.universityGroup):
        raise PermissionDenied
    resp = {
        'id': id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'patronymic': user.patronymic,
    }
    if user.universityGroup:
        resp['universityGroup'] = user.universityGroup.name
    if user.is_admin or user.is_deanery:
        resp['notStudent'] = True
    return JsonResponse(resp)

# -*- encoding: utf-8 -*-
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response


# Create your views here.

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

def login(request):
    if request.method == 'POST':  
        uf = LoginForm(request.POST)  
        if uf.is_valid():  
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']
            # user = User.objects.filter(username__exact = username,password__exact = password)  
            # if user:  
            #     request.session['username'] = username  
            #     return HttpResponseRedirect('/blog/index')  
            # else:  
            #     err = 'incorrect username or pwd,please input again.'  
            #     return render_to_response('login.html',{'err':err})  
            if username=='admin' and password=='a':
                #request.session['username'] = username
                return HttpResponseRedirect('/crawlermanage/index')
            else:
                return render_to_response('crawlermanage/login.html', {'error': '用户名或密码错误'})

    else:
        return render_to_response('crawlermanage/login.html')

def index(request):
    return render(request, 'crawlermanage/index.html')

def tasks(request):
    return render(request, 'crawlermanage/tasks.html')

def taskdata(request):
    return render(request, 'crawlermanage/taskdata.html')

def layout(request):
    return render(request, 'crawlermanage/layout.html')


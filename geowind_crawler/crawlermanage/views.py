from django.shortcuts import render

# Create your views here.

def home(request):
	return render(request, 'crawlermanage/login.html')

def login(request):
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	if username == 'admin' and password == 'a':
		return render(request, 'crawlermanage/index.html')
	else:
		return render(request, 'crawlermanage/index.html')


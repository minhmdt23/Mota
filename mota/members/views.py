from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile
from django.core.files.storage import FileSystemStorage
from django.templatetags.static import static



# Create your views here.

def login_user(request):

	if request.user.is_authenticated:
		return redirect('home')

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('home')
		else:
			messages.success(request, ("Tài khoảng hoặc mật khẩu bị sai."))
			return redirect('login')
	else:
		context = {}
		return render(request, 'members/login.html', context)


def logout_user(request):
	logout(request)
	messages.success(request, ("Đăng xuất thành công."))
	return redirect('login')


def register_user(request):
	if request.user.is_authenticated:
		return redirect('home')

	if request.method == 'POST':
		username = request.POST['username']
		password1 = request.POST['password1']
		password2 = request.POST['password2']
		email = request.POST['email']

		try:
			user = User.objects.get(username=username)
			messages.success(request, ("Tên người dùng đã tồn tại."))
			return redirect('register')
		except:
			if(password1 == password2):
				user = User.objects.create_user(username=username, email=email, password=password1)
				userprofile = UserProfile(user=user)
				userprofile.save()
				login(request, user)
				return redirect('home')
			else:
				messages.success(request, ("Mật khẩu không khớp."))
				return redirect('register')
	else:
		context = {}
		return render(request, 'members/register.html', context)

def upload_user_avatar(request):
	if request.user.is_authenticated:
		if request.method == 'POST' and request.FILES['avatar']:
			upload = request.FILES['avatar']
			fss = FileSystemStorage(base_url='/'+str(request.user.id))
			file = fss.save(upload.name, upload)
			file_url = fss.url(file)

			avatar = request.FILES['avatar']
			userprofile = UserProfile.objects.get(user=request.user)
			userprofile.avatar = avatar
			userprofile.save()
			return redirect('home')

	else:
		return redirect('login')

	context = {}
	return render(request, 'members/upload_user_avatar.html', context)
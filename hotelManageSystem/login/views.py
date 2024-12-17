from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserLoginForm, UserRegisterForm
from publicModels.models import User
from django.contrib.auth.decorators import login_required

# 登录视图
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"欢迎回来，{username}！")
                
                # 根据用户的角色重定向
                if user.role == 'front_desk':  # 如果是前台用户
                    return redirect('customerInfor')  # 前台的页面
                elif user.role == 'ac_manager':  # 如果是空调管理员
                    return redirect('acmanage')  # 空调管理员的页面
                elif user.role == 'hotel_manager':  # 如果是酒店经理
                    return redirect('index')  # 酒店经理的页面
                else:
                    return redirect('index')  # 默认跳转到首页
            else:
                messages.error(request, "用户名或密码错误")
        else:
            messages.error(request, "表单无效")
    else:
        form = UserLoginForm()
    
    return render(request, 'login.html', {'form': form})  # 渲染登录页面

# 注册视图
def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # 不直接保存
            user.set_password(form.cleaned_data['password'])  # 使用 set_password 来加密密码
            user.save()  # 保存用户
            messages.success(request, "注册成功！请登录。")
            return redirect('login')  # 注册成功后跳转到登录页面
        else:
            # 如果表单无效，打印出具体的错误
            for field in form.errors:
                for error in form.errors[field]:
                    messages.error(request, f"{field} - {error}")  # 将表单字段的错误传递给前端
    else:
        form = UserRegisterForm()
    
    return render(request, 'register.html', {'form': form})  # 渲染注册页面

# 首页视图，登录后才能访问
@login_required(login_url='/login/')
def index(request):
    # 获取当前用户的身份
    user_identity = dict(User.ROLE_CHOICES).get(request.user.role, '未知身份')
    return render(request, 'index.html', {'identity': user_identity, 'username': request.user.username})  # 指定login目录下的index.html模板

# 登出视图
def user_logout(request):
    logout(request)  # 注销用户
    messages.success(request, "您已成功登出。")
    return redirect('login')  # 登出后跳转到登录页面

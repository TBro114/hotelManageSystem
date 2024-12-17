from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('index/', views.index, name='index'),
    path('logout/', views.user_logout, name='logout'),  # 添加登出路由
]

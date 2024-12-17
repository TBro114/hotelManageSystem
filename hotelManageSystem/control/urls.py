from django.urls import path
from . import views

urlpatterns = [
    path('', views.controlPanel, name='control'),
    path('login',views.login,name='customerloginlogin'),
    path('logout/', views.logout_view, name='customerlogout'),
    path('update-air-condition/', views.update_air_condition, name='update_air_condition'),
    path('get-air-condition/', views.get_air_condition,name='get_air_condition'),
]
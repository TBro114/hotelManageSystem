from django.urls import path
from . import views

urlpatterns = [
    path('', views.acmanage, name='acmanage'),
    path('get-center-aircondition/',views.get_center_aircondition,name='get_center_aircondition'),
    path('update-center-aircondition/', views.update_center_aircondition, name='update_center_aircondition'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('customerInfor', views.customerInfor,name="customerInfor"),
    path('roomInquiry',views.roomInquiry,),
]

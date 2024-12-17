from django.urls import path
from . import views

urlpatterns = [
    path('charge', views.charge),
    path('acDetailRecord',views.acDetailRecord),
    path('charge/billDownload',views.export_to_excel)
]

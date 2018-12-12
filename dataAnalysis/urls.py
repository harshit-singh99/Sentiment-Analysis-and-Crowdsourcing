from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from . import views

urlpatterns = [
    path('', views.main_view, name='data_analysis'),
    path('da_show_list/', views.show_list, name='da_show_list'),
    path('stats/', views.stats, name='stats'),
]
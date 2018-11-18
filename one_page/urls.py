from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from . import views

urlpatterns = [
    path('', views.main_view, name='review'),
    path('show_list/', views.show_list, name='show_list'),
    path('show_reviews/', views.show_reviews, name='show_reviews'),
    path('write_review', views.write_review, name='write_reviews'),
]
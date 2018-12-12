from django.urls import path
from . import views



urlpatterns = [
    path('', views.crd_scr_get, name='crdscr_main'),
    path('nxt/', views.crd_scr_post, name='crdscr_next'),
]
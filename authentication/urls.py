from django.urls import path
from django.conf.urls import include
from . import views

urlpatterns = [

    path('login/', views.login_view,name = 'signin'),
    path('logout/', views.logout_view , name = 'logout'),
    path('signup/', views.signup_view,name = 'signup'),
    path('', include('django.contrib.auth.urls')),
]

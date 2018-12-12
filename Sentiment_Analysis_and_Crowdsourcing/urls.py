"""Sentiment_Analysis_and_Crowdsourcing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from . import  views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('authentication.urls')),
    path('auth/', include('social_django.urls', namespace='social')),
    path('', views.home, name='home'),
    path('predict/', include('predictReview.urls')),
    path('review/', include('one_page.urls')),
    path('credits/',include('credits.urls')),
    path('data_analysis/', include('dataAnalysis.urls')),
    path('crowdsourcing/', include('crowdSourcing.urls')),
    path('api/', include('api.urls')),
    path('crowdsourcing/', include('crowdSourcing.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
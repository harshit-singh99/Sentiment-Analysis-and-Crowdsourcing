from django.urls import path
from . import views

urlpatterns = [
    path('', views.predict_review, name='prediction'),
    path('batchpredict/', views.batch_predict, name = 'batch_predict'),
]
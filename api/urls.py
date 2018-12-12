from . import views
from django.urls import path

urlpatterns = [
    path('movie/', views.MovieView.as_view()),
    path('rests/', views.RestsView.as_view()),
    path('predict/', views.Predict.as_view())
]

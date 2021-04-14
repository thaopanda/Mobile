from django.contrib import admin
from django.urls import path
from Favorite import views

urlpatterns = [
    path('createDelete/<int:pk>/', views.CreateAndDeleteFavorite.as_view()),
]

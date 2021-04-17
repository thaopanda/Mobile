from django.contrib import admin
from django.urls import path
from Rating import views

urlpatterns = [
    path('createAndUpdateRating/', views.CreateAndUpdateRating.as_view()),
]

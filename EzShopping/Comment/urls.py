from django.contrib import admin
from django.urls import path
from Comment import views

urlpatterns = [
    path('createComment/', views.CreateComment.as_view()),
    path('getProductComment/<int:pk>/<int:begin>/<int:end>/', views.GetProductComment.as_view()),
]

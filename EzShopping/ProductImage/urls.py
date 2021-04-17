from django.contrib import admin
from django.urls import path
from ProductImage import views

urlpatterns = [
    path('getProductImage/', views.GetProductImage.as_view()),
]

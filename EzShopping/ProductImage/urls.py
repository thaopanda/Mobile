from django.contrib import admin
from django.urls import path
from ProductImage import views

urlpatterns = [
    path('getProductImage/<int:pk>/<int:begin>/<int:end>/', views.GetProductImage.as_view()),
]

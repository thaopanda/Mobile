from django.contrib import admin
from django.urls import path
from Comment import views

urlpatterns = [
    path('createAndUpdateComment/', views.CreateAndUpdateComment.as_view()),
    path('getProductComment/', views.GetProductComment.as_view()),
    # path('updateComment/<int:pk>/', views.UpdateComment.as_view()),
]

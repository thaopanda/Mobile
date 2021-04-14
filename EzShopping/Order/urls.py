from django.contrib import admin
from django.urls import path
from Order import views

urlpatterns = [
    path('create/', views.CreateOrderView.as_view()),
    path('listOrderOfCustomer/', views.GetListOrderOfCustomer.as_view()),
    path('listOrderOfShop/', views.GetListOrderOfShop.as_view()),
    path('acceptOrder/<int:pk>/', views.AcceptNewOrder.as_view()),
    path('denyOrder/<int:pk>/', views.DeniedNewOrder.as_view()),

]

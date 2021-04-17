from django.contrib import admin
from django.urls import path
from Order import views

urlpatterns = [
    path('create/', views.CreateOrderView.as_view()),
    path('listOrderOfCustomer/', views.GetListOrderOfCustomer.as_view()),
    path('listOrderOfShop/', views.GetListOrderOfShop.as_view()),
    path('changeOrderStatus/', views.ChangeOrderStatus.as_view()),
    path('orderDetail/', views.GetOrderDetail.as_view()),

]

from django.contrib import admin
from django.urls import path
from Product_In_Cart import views

urlpatterns = [
    path('productCart/', views.ProductCartView.as_view()),
    path('getListProductCart/', views.GetListProductInCart.as_view()),
    path('deleteProductCart/', views.DeleteProductCart.as_view()),
]

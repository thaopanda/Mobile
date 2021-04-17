from django.contrib import admin
from django.urls import path
from Product import views

urlpatterns = [
    path('create/', views.CreateProductView.as_view()),
    path('update/', views.UpdateProductView.as_view()),
    path('productdetail/', views.GetProductDetail.as_view()),
    path('productOfShop/', views.GetListProductOfShop.as_view()),
    path('searchbyciteria/', views.SearchByCiteria.as_view()),
    path('searchbyclass/', views.SearchByClass.as_view()),
    path('delete/<int:pk>/', views.DeleteProduct.as_view()),
]

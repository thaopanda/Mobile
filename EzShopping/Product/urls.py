from django.contrib import admin
from django.urls import path
from Product import views

urlpatterns = [
    path('create/', views.CreateProductView.as_view()),
    path('update/<int:pk>/', views.UpdateProductView.as_view()),
    path('productdetail/<int:pk>/', views.GetProductDetail.as_view()),
    path('productOfShop/<str:pk>/<int:begin>/<int:end>/', views.GetListProductOfShop.as_view()),
    path('searchbyciteria/', views.SearchByCiteria.as_view()),
    path('searchbyclass/', views.SearchByClass.as_view()),
]

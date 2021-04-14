from django.contrib import admin
from django.urls import path
from User import views

urlpatterns = [
    path('customerregister/', views.CustomerRegistrationView.as_view()),
    path('sellerregister/', views.SellerRegistrationView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('customerprofile/', views.CustomerProfileView.as_view()),
    path('sellerprofile/', views.SellerProfileView.as_view()),
    path('customerupdateprofile/', views.CustomerUpdateProfileView.as_view()),
    path('sellerupdateprofile/', views.SellerUpdateProfileView.as_view()),
    path('sellerlist/<int:begin>/<int:end>/', views.GetListSeller.as_view()),
    path('setavatar/', views.SetAvatar.as_view()),
    path('changePassword/', views.ChangePassword.as_view()),
]

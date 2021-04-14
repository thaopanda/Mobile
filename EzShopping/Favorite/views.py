from django.shortcuts import render
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.validators import RegexValidator
from datetime import datetime, timedelta, timezone, tzinfo
import django_filters
from rest_framework import generics
from django_filters import rest_framework as rf
from Product.models import Product
from User.models import MyUser, Customer, Seller
from Favorite.models import Favorite

class CreateAndDeleteFavorite(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request,pk, format=None):
        user = Customer.objects.get(email=request.user.email)
        product = Product.objects.get(pk=pk)
        favorite = Favorite.objects.filter(customer=user, product=product)
        if(len(favorite)!=0):
            product.total_like = product.total_like-1
            product.save()
            favorite[0].delete()
        else:
            product.total_like = product.total_like+1
            product.save()
            Favorite.objects.createFavorite(user,product)
        return Response(f'ok')
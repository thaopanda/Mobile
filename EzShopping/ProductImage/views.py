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
from ProductImage.models import ProductImage

class GetProductImage(APIView):
    permission_classes = (AllowAny,)
    class ProductImageSerializer(serializers.ModelSerializer):
        class Meta:
            model = ProductImage
            fields = ['image']

    def get(self, request, pk, begin, end, format = None):
        image = ProductImage.objects.filter(product=pk)[begin:end]
        serializer = self.ProductImageSerializer(image, many=True)
        return Response(serializer.data)


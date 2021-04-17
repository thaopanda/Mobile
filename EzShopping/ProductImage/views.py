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

    def get(self, request, format = None):
        try:
            pk = request.query_params['product']
            query_type = request.query_params['type']
            if(query_type=="all"):
                image = ProductImage.objects.filter(product=pk)[1:]
            else:
                image = ProductImage.objects.filter(product=pk)[0:1]
            serializer = self.ProductImageSerializer(image, many=True)
            image = list()
            for i in serializer.data:
                image.append(i['image'])
            response = {
                "success":True,
                "image":image
            }
            return Response(response)
        except Exception:
            response = {
                "success":False,
            }
            return Response(response)


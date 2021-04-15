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
from Product_In_Cart.models import Product_In_Cart

class ProductCartView(APIView):
    permission_classes = (IsAuthenticated,)

    class ProductCartSerializer(serializers.ModelSerializer):
        # customer = serializers.SlugRelatedField(
        #     read_only=True, slug_field='fullname', many=True)
        product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
        amount = serializers.FloatField()

        class Meta:
            model = Product_In_Cart
            fields = ['id','amount', 'product' ]

    def post(self, request, format=None):
        serializer = self.ProductCartSerializer(data=request.data)
        if(serializer.is_valid()):
            customer = Customer.objects.get(email=request.user.email)
            serializer.save(customer=customer)
            return Response(f'ok')
        return Response(f'This product have been delete or cannot found this product')

class GetListProductInCart(APIView):
    class ProductInCartList(serializers.ModelSerializer):
        class Meta:
            model = Product_In_Cart
            fields = ['amount', 'product']

    def get(self, request, format=None):
        product_in_cart = Product_In_Cart.objects.filter(customer = request.user)
        serializer = self.ProductInCartList(product_in_cart, many=True)
        for i in serializer.data:
            product = Product.objects.get(pk = i['product'])
            i['product'] = {'id':product.id, 'product_name':product.product_name, 'headImage':product.headImage}
        return Response(serializer.data)

class DeleteProductCart(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, pk, format=None):
        product_in_cart = Product_In_Cart.objects.get(pk=pk)
        if(request.user.email == product_in_cart.customer.email):
            product_in_cart.delete()
            return Response(f'ok')
        return Response(f'Dont have permission to delete')
    

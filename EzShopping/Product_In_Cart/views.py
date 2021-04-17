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
        product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
        amount = serializers.FloatField()

        class Meta:
            model = Product_In_Cart
            fields = ['id','amount', 'product' ]

    def post(self, request, format=None):
        productInCart = Product_In_Cart.objects.filter(product = request.data['product'], customer = request.user)
        if(len(productInCart)>0):
            try:
                amount = request.data['amount']
                productInCart[0].amount = productInCart[0].amount+ int(amount)
                productInCart[0].save()
            except:
                response = {
                    "success":False,
                    "msg": "Do not provide amount"
                }
                return Response(response)
            response = {
                "success": True,
                "msg":"Add more amount to product in cart"
            }
            return Response(response)
        else:
            serializer = self.ProductCartSerializer(data = request.data)
            customer = Customer.objects.get(email=request.user.email)
            if(serializer.is_valid()):
                serializer.save(customer=customer)
                response = {
                    "success":True,
                    "msg": "Add product to cart"
                }
                return Response(response)
            response = {
                "success":False,
                "msg":"Not enough data to add product to cart"
            }
            return Response(response)

class GetListProductInCart(APIView):
    class ProductInCartList(serializers.ModelSerializer):
        class Meta:
            model = Product_In_Cart
            fields = ['id','amount', 'product']

    def get(self, request, format=None):
        try:
            product_in_cart = Product_In_Cart.objects.filter(customer = request.user)
            serializer = self.ProductInCartList(product_in_cart, many=True)
            for i in serializer.data:
                product = Product.objects.get(pk = i['product'])
                i['product'] = {'id':product.id, 'product_name':product.product_name}
            return Response(serializer.data)
        except Exception:
            response = {
                "success":False
            }
            return Response(response)

class DeleteProductCart(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, format=None):
        try:
            pk = request.query_params['product_in_cart']
            product_in_cart = Product_In_Cart.objects.get(pk=pk)
            if(request.user.email == product_in_cart.customer.email):
                product_in_cart.delete()
                response = {
                    "success":True
                }
                return Response(response)
        except Exception:
            response = {
                "success":False,
                "msg":"cannot find this product_in_cart"
            }
            return Response(response)
    

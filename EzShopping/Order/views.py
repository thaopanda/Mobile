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
from User.models import Customer, Seller
from Product.models import Product
from Order.models import Order
from OrderDetail.models import OrderDetail

PAGE_SIZE = 5

class CreateOrderView(APIView):
    permission_classes = (IsAuthenticated,)
    class OrderSerializer(serializers.ModelSerializer):
        seller = serializers.SlugRelatedField(
            read_only=True, slug_field='fullname', many=True)
        customer = serializers.SlugRelatedField(
            read_only=True, slug_field='fullname', many=True)
        class Meta:
            model = Order
            fields = ['id', 'customer', 'seller']

    def post(self, request, format=None):
        msg="Cannot create order"
        try:
            ship_cost=0.0
            msg = "Not provide orderDetail"
            orderDetail = request.data['orderDetail']
            print(orderDetail)
            product = Product.objects.get(pk=orderDetail[0]['product'])
            msg = "Cannot create order"
            customer = Customer.objects.get(email=request.user.email)
            order = Order.objects.CreateOrder(seller=product.seller, customer=customer, order_status="waiting", ship_cost=ship_cost)
            print(order)
            product_cost = 0
            for i in orderDetail:
                product = Product.objects.get(pk=i['product'])
                product_cost += i['amount']* product.price
                OrderDetail.objects.CreateOrderDetail(order=order, product=product, amount=i['amount'])
            order.product_cost = product_cost
            order.save()
            response = {
                "success":True
            }
            return Response(response)
        except Exception:
            
            response = {
                "success":False,
                "msg":msg
            }
            return Response(response)

# get list order following status
class GetListOrderOfCustomer(APIView):
    class ListOrderSerializer(serializers.ModelSerializer):
        class Meta:
            model = Order
            fields = ['id','order_status', 'ship_cost', 'product_cost']

    def get(self, request, format=None):
        try:
            page = request.query_params['page']
            end = int(page)*PAGE_SIZE
            begin = end-PAGE_SIZE
            order = Order.objects.filter(customer = request.user)[begin: end]
            serializer = self.ListOrderSerializer(order, many=True)

            # detail = OrderDetail.objects.filter
            # for i in serializer.data:
            #     product = Product.objects.get(pk = i['product'])
            #     i['product'] = {'product_name':product.product_name}
            return Response(serializer.data)
        except Exception:
            response = {
                "success":False
            }
            return Response(response)

class GetListOrderOfShop(generics.ListAPIView):
    class ListOrderSerializer(serializers.ModelSerializer):
        class Meta:
            model = Order
            fields = ['id','order_status', 'ship_cost', 'product_cost']

    class OrderFilter(django_filters.FilterSet):
        order_status = django_filters.CharFilter(
        field_name='order_status', lookup_expr='iexact')

        class Meta:
            model = Order
            fields = ['order_status']

    
    serializer_class = ListOrderSerializer
    filter_backends = (rf.DjangoFilterBackend,)
    filterset_class = OrderFilter

    def list(self, request, *args, **kwargs):
        try:
            page = request.query_params['page']
            end = int(page)*PAGE_SIZE
            begin = end-5
            seller = Seller.objects.get(email = request.user.email)
            queryset = Order.objects.filter(seller=seller)[begin:end]
            serializer = self.get_serializer(queryset, many=True)

            # for i in serializer.data:
            #     product = Product.objects.get(pk = i['product'])
            #     i['product'] = {'product_name':product.product_name}
            return Response(serializer.data)
        except Exception:
            response = {
                "success":False
            }
            return Response(response)

class GetOrderDetail(APIView):
    class OrderDetailSerializer(serializers.ModelSerializer):
        class Meta:
            model = OrderDetail
            fields = ['product', 'amount']

    def get(self, request, format=None):
        try:
            order = request.query_params['order']
            orderDetail = OrderDetail.objects.filter(order=order)
            serializer = self.OrderDetailSerializer(orderDetail, many=True)
            response = {
                "success":True,
                "orderDetail": serializer.data
            } 
            return Response(response)
        except Exception:
            response = {
                "success":False
            }
            return Response(response)

class ChangeOrderStatus(APIView):
    def put(self, request, format=None):
        try:
            pk = request.query_params['order']
            order = Order.objects.get(pk=pk)
            order.order_status = request.data['order_status']
            order.save()
            response = {
                "success":True
            }
            return Response(response)
        except Exception:
            response = {
                "success":False
            }
        return Response(response)
        
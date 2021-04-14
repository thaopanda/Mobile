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

class CreateOrderView(APIView):
    permission_classes = (IsAuthenticated,)

    class CreateOrderSerializer(serializers.ModelSerializer):
        customer = serializers.SlugRelatedField(
            read_only=True, slug_field='fullname', many=True)
        # seller = serializers.SlugRelatedField(
        #     read_only=True, slug_field='fullname', many=True)
        # product = serializers.SlugRelatedField(
        #     read_only=True, slug_field='fullname', many=True)
        product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
        amount = serializers.FloatField()
        ship_cost =serializers.FloatField()

        class Meta:
            model = Order
            fields = ['id','customer', 'product', 'amount', 'ship_cost']

    def post(self, request, format=None):
        serializer = self.CreateOrderSerializer(data=request.data)

        if(serializer.is_valid()):
            customer = Customer.objects.get(email=request.user.email)
            product = serializer.validated_data['product']
            print(product)
            print(product.seller)
            serializer.save(customer=customer, order_status='waiting', seller= product.seller)
            return Response(f'ok')
        return Response(f'not ok')

# get list order following status
class GetListOrderOfCustomer(APIView):
    class ListOrderSerializer(serializers.ModelSerializer):
        class Meta:
            model = Order
            fields = ['order_status', 'amount', 'ship_cost', 'product']

    def get(self, request, format=None):
        order = Order.objects.filter(customer = request.user)
        serializer = self.ListOrderSerializer(order, many=True)
        for i in serializer.data:
            product = Product.objects.get(pk = i['product'])
            i['product'] = {'product_name':product.product_name, 'headImage':product.headImage}
        return Response(serializer.data)

class GetListOrderOfShop(generics.ListAPIView):
    class ListOrderSerializer(serializers.ModelSerializer):
        class Meta:
            model = Order
            fields = ['order_status', 'amount', 'ship_cost', 'product']

    class OrderFilter(django_filters.FilterSet):
        order_status = django_filters.CharFilter(
        field_name='order_status', lookup_expr='iexact')

        class Meta:
            model = Order
            fields = ['order_status']

    queryset = Order.objects.all()
    serializer_class = ListOrderSerializer
    filter_backends = (rf.DjangoFilterBackend,)
    filterset_class = OrderFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        for i in serializer.data:
            product = Product.objects.get(pk = i['product'])
            i['product'] = {'product_name':product.product_name, 'headImage':product.headImage}
    
        return Response(serializer.data)

class AcceptNewOrder(APIView):
    def put(self, request, pk, format=None):
        order = Order.objects.get(pk=pk)
        print(request.user.username)
        print(order.seller)
        # if request.user.username == order.seller:
        order.order_status = 'accepted'
        order.save()
        return Response(f'ok')
        # return Response(f'not ok')

class DeniedNewOrder(APIView):
    def put(self, request, pk, format=None):
        order = Order.objects.get(pk=pk)
        # if request.user.username == order.seller:
        order.order_status = 'denied'
        order.save()
        return Response(f'ok')
        # return Response(f'not ok')
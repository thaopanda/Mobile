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
from Favorite.models import Favorite
from Rating.models import Rating

class CreateProductView(APIView):
    permission_classes = (IsAuthenticated,)

    class CreateProductSerializer(serializers.ModelSerializer):
        seller = serializers.SlugRelatedField(
            read_only=True, slug_field='fullname', many=True)
        product_name = serializers.CharField()
        price = serializers.IntegerField()
        description = serializers.CharField()
        unit = serializers.CharField()
        in_stock = serializers.IntegerField()
        status = serializers.CharField()
        product_class = serializers.CharField(max_length=30)
        vendor = serializers.CharField(max_length=100)
        # headImage = serializers.ListField(child=serializers.CharField())

        class Meta:
            model = Product
            fields = ['id','product_name', 'price', 'description','unit', 'in_stock', 'status', 'product_class', 'seller', 'vendor' ]

    def post(self, request, format=None):
        serializer = self.CreateProductSerializer(data=request.data)
        image = serializer.initial_data['headImage']
        if(serializer.is_valid()):
            seller = Seller.objects.get(email=request.user.email)
            product = serializer.save(seller=seller)
            for i in range(len(image)):
                ProductImage.objects.CreateProductImage(product=product, image=image[i], priority=i+1)
            response = {
                "success":True
            }
            return Response(response)
        response={
            "success":False
        }
        return Response(response)

class UpdateProductView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, format=None):
        pk = request.query_params['product']
        product = Product.objects.get(pk=pk)
        
        try:
            product.product_name = request.data['product_name']
        except Exception:
            pass

        try:
            product.price = request.data['price']
        except Exception:
            pass

        try:
            product.description = request.data['description']
        except Exception:
            pass
        
        try:
            product.vendor= request.data['vendor']
        except Exception:
            pass

        try:
            product.unit = request.data['unit']
        except Exception:
            pass

        try:
            product.in_stock = request.data['in_stock']
        except Exception:
            pass
        try:
            product.status = request.data['status']
        except Exception:
            pass
        try:
            product.product_class = request.data['product_class']
        except Exception:
            pass
        product.save()

        try:
            image = request.data['image']
            productImage = ProductImage.objects.filter(product=product)
            for i in productImage:
                i.delete()
            for i in range(len(image)):
                ProductImage.objects.CreateProductImage(product=product, image=image[i], priority=i)
        except Exception:
            response = {
                "success":False
            }
            return Response(response)

        response = {
            'success':True
        }
        return Response(response)

class GetProductDetail(APIView):
    permission_classes = (AllowAny,)

    class ProductDetailSerializer(serializers.ModelSerializer):
        class Meta:
            model = Product
            fields = '__all__'

    def get(self, request, format=None):
        try:
            pk = request.query_params['product']
        except Exception:
            response = {
                "success":False,
                "msg": "Not provide productID"
            }
            pass
        productDetail = Product.objects.filter(pk=pk)
        
        serializer = self.ProductDetailSerializer(productDetail, many=True)
        for i in serializer.data:
            i['seller'] = Seller.objects.get(pk=i['seller']).fullname
        if(request.user.is_anonymous or request.user.user_type == 'renter'):
            productDetail[0].total_views = productDetail[0].total_views + 1
            productDetail[0].save()
        if(request.user.is_anonymous == False):
            favortie = Favorite.objects.filter(product=pk, customer = request.user)
            rating = Rating.objects.filter(product=pk, customer = request.user)
            if(len(favortie)>0):
                serializer.data[0]['like'] = True
            else:
                serializer.data[0]['like'] = False

            if(len(rating)>0):
                serializer.data[0]['rating'] = rating[0].rating

        if(serializer.data[0]['commentNum']==0):
            serializer.data[0]['averageRate'] = "Not have rate yet"
        return Response(serializer.data[0])

class GetListProductOfShop(APIView):
    class ListProductOfShop(serializers.ModelSerializer):
        class Meta:
            model = Product
            fields = '__all__'
    
    def get(self, request,format=None):
        try:
            page = request.query_params['page']
            begin = 5*(int(page)-1)
            end = 5*int(page)
        except Exception:
            response = {
                "success":False,
                "msg": "Dont have page number"
            }
            return Response(response)
        seller = Seller.objects.filter(username=str(request.user.username))
        product = Product.objects.filter(seller = seller[0])[begin:end]
        serializer = self.ListProductOfShop(product, many=True)
        return Response(serializer.data)

class SearchByCiteria(generics.ListAPIView):
    
    class SearchSerializer(serializers.ModelSerializer):
        class Meta:
            model = Product
            fields = '__all__'

    class SearchFilter(django_filters.FilterSet):
        vendor = django_filters.CharFilter(
        field_name='vendor', lookup_expr='icontains')
        product_name = django_filters.CharFilter(
            field_name='product_name', lookup_expr='icontains')
        price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

        class Meta:
            model = Product
            fields = ['vendor', 'product_name', 'price']
    serializer_class = SearchSerializer
    filter_backends = (rf.DjangoFilterBackend,)
    filterset_class = SearchFilter

    def list(self, request, *args, **kwargs):
        try:
            page = request.query_params['page']
            begin = 5*(int(page)-1)
            end = 5*int(page)
        except Exception:
            response = {
                "success":False,
                "msg": "Dont have page number"
            }
            return Response(response)

        queryset = Product.objects.all()[begin:end]
        serializer = self.get_serializer(queryset, many=True)
        for i in serializer.data:
            if(request.user.is_anonymous == False):
                favortie = Favorite.objects.filter(product=i['id'], customer = request.user)
                if(len(favortie)>0):
                    i['like'] = True
                else:
                    i['like'] = False
        
        return Response(serializer.data)

class SearchByClass(generics.ListAPIView):
    class SearchByClassSerializer(serializers.ModelSerializer):
        class Meta:
            model = Product
            fields = '__all__'

    class SearchByClassFilter(django_filters.FilterSet):
        product_class = django_filters.CharFilter(
        field_name='product_class', lookup_expr='iexact')

        class Meta:
            model = Product
            fields = ['product_class']
    serializer_class = SearchByClassSerializer
    filter_backends = (rf.DjangoFilterBackend,)
    filterset_class = SearchByClassFilter

    def list(self, request, *args, **kwargs):
        try:
            page = request.query_params['page']
            begin = 5*(int(page)-1)
            end = 5*int(page)
        except Exception:
            response = {
                "success":False,
                "msg": "Dont have page number"
            }
            return Response(response)

        queryset = Product.objects.all()[begin:end]
        serializer = self.get_serializer(queryset, many=True)
        for i in serializer.data:
            if(request.user.is_anonymous == False):
                favortie = Favorite.objects.filter(product=i['id'], customer = request.user)
                if(len(favortie)>0):
                    i['like'] = True
                else:
                    i['like'] = False
        
        return Response(serializer.data)

class DeleteProduct(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, pk, format=None):
        product = Product.objects.get(pk=pk)
        print(request.user)
        print(product.seller.email)
        if(request.user.email == product.seller.email):
            product.delete()
            response = {
                "success":True
            }
            return Response(response)
        response = {
            "success":False
        }
        return Response(response)

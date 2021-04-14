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
from Comment.models import Comment

class CreateComment(APIView):
    permission_classes = (IsAuthenticated,)
    class CommentSerializer(serializers.ModelSerializer):
        customer = serializers.SlugRelatedField(
            read_only=True, slug_field='username', many=True)
        rating = serializers.IntegerField()
        class Meta:
            model = Comment
            fields = ['content', 'image', 'product', 'customer', 'rating']

    def post(self, request, format = None):
        serializer = self.CommentSerializer(data=request.data)
        if(serializer.is_valid()):
            user = Customer.objects.get(email=request.user)
            serializer.save(customer=user)
            total_comment = serializer.validated_data['product'].commentNum +1
            serializer.validated_data['product'].commentNum = total_comment
            serializer.validated_data['product'].save()
            return Response(f'ok')
        return Response(f'not ok')

class GetProductComment(APIView):
    class ProductCommentSerializer(serializers.ModelSerializer):
        # customer = serializers.SlugRelatedField(
        #     read_only=True, slug_field='fullname')
        class Meta:
            model = Comment
            fields = ['content', 'image', 'customer']

    def get(self, request, pk, begin, end, format=None):
        comment = Comment.objects.filter(product=pk)
        serializer = self.ProductCommentSerializer(comment, many=True)
        for i in serializer.data:
            customer = Customer.objects.get(id=i['customer'])
            i['customer'] = {'username':customer.username, 'image':customer.image}
        return Response(serializer.data)


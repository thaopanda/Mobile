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

class CreateAndUpdateComment(APIView):
    permission_classes = (IsAuthenticated,)
    class CommentSerializer(serializers.ModelSerializer):
        customer = serializers.SlugRelatedField(
            read_only=True, slug_field='username', many=True)
        rating = serializers.IntegerField()
        class Meta:
            model = Comment
            fields = ['content', 'image', 'product', 'customer', 'rating']

    def post(self, request, format = None):
        print(request.data)
        comment = Comment.objects.filter(product=request.data['product'], customer= request.user)
        if len(comment)>0:
            serializer = self.CommentSerializer(comment[0], data=request.data)
            if(serializer.is_valid()):
                serializer.save()
                allComment = Comment.objects.filter(product=request.data['product'])
                totalRate = 0
                for i in allComment:
                    totalRate+= i.rating
                averageRate = round(totalRate/len(allComment),1)
                product = Product.objects.get(pk=request.data['product'])
                product.averageRate = averageRate
                product.save()
                return Response(f'Update successfully')
            return Response('Lack information to update')
        else:
            serializer = self.CommentSerializer(data=request.data)
            if(serializer.is_valid()):
                user = Customer.objects.get(email=request.user)
                serializer.save(customer=user)
                total_comment = serializer.validated_data['product'].commentNum +1
                serializer.validated_data['product'].commentNum = total_comment
                serializer.validated_data['product'].save()

                allComment = Comment.objects.filter(product=request.data['product'])
                totalRate = 0
                for i in allComment:
                    totalRate+= i.rating
                averageRate = round(totalRate/len(allComment),1)
                product = Product.objects.get(pk=request.data['product'])
                product.averageRate = averageRate
                product.save()
                return Response(f'Create comment successfully')
            return Response(f'Lake information to create comment')

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

# class UpdateComment(APIView):
#     permission_classes = (IsAuthenticated,)
#     class UpdateCommentSerializer(serializers.ModelSerializer):
#         rating = serializers.IntegerField()
#         class Meta:
#             model = Comment
#             fields = ['content', 'image', 'product','rating']

#     def put(self, request, pk, format = None):
#         comment = Comment.objects.get(pk=pk)
#         serializer = self.UpdateCommentSerializer(comment, data=request.data)
#         if(serializer.is_valid()):
#             serializer.save()
#             return Response(f'ok')
#         return Response(f'not ok')
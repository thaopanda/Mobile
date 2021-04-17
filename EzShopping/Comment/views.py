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
        class Meta:
            model = Comment
            fields = ['content', 'image', 'product', 'customer']

    def post(self, request, format = None):
        comment = Comment.objects.filter(product=request.data['product'], customer= request.user)
        if len(comment)>0:
            try:
                content = request.data['content']
                comment[0].content = content
                comment[0].save()
            except Exception:
                pass

            try:
                image = request.data['image']
                comment[0].image = image
                comment[0].save()
            except Exception:
                pass
            response = {
                "success":True,
                "msg":"Update comment successfully"
            }
                
            return Response(response)
        else:
            serializer = self.CommentSerializer(data=request.data)
            if(serializer.is_valid()):
                user = Customer.objects.get(email=request.user)
                serializer.save(customer=user)
                total_comment = serializer.validated_data['product'].commentNum +1
                serializer.validated_data['product'].commentNum = total_comment
                serializer.validated_data['product'].save()
                response = {
                    "success":True,
                    "msg":'Create comment successfully'
                }
                return Response(response)
            response = {
                "success":False,
                "msg":'Lack information to create comment'
            }
            return Response(response)

class GetProductComment(APIView):
    class ProductCommentSerializer(serializers.ModelSerializer):
        class Meta:
            model = Comment
            fields = ['content', 'image', 'customer']

    def get(self, request, format=None):
        try:
            pk = request.query_params['product']
            page = request.query_params['page']
            end = 5*int(page)
            begin = end-5
            comment = Comment.objects.filter(product=int(pk))[begin:end]
        except Exception:
            response = {
                "success":False,
                "msg":"Not provide productID"
            }
            return Response(response)
        serializer = self.ProductCommentSerializer(comment, many=True)
        for i in serializer.data:
            customer = Customer.objects.get(id=i['customer'])
            i['customer'] = {'username':customer.username, 'image':customer.image}
            response = {
                "success":True,
                "comment":serializer.data
            }
        return Response(response)

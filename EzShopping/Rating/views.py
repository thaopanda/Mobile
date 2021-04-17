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
from Rating.models import Rating

class CreateAndUpdateRating(APIView):
    permission_classes = (IsAuthenticated,)
    class RatingSerializer(serializers.ModelSerializer):
        class Meta:
            model = Rating
            fields = ['product', 'rating' ]

    def post(self, request, format = None):
        rating = Rating.objects.filter(product=request.data['product'], customer= request.user)
        if len(rating)>0:
            serializer = self.RatingSerializer(rating[0], data=request.data)
            if(serializer.is_valid()):
                serializer.save()
                allRating = Rating.objects.filter(product=request.data['product'])
                totalRate = 0
                for i in allRating:
                    totalRate+= i.rating
                averageRate = round(totalRate/len(allRating),1)
                product = Product.objects.get(pk=request.data['product'])
                product.averageRate = averageRate
                product.save()
                response = {
                    "success":True,
                    "msg":"Update rating successfully"
                }
                return Response(response)
            response = {
                "success":False,
                "msg":"Update rating unsuccessfully"
            }
            return Response(response)
        else:
            serializer = self.RatingSerializer(data=request.data)
            if(serializer.is_valid()):
                user = Customer.objects.get(email=request.user)
                serializer.save(customer=user)

                allRating = Rating.objects.filter(product=request.data['product'])
                totalRate = 0
                for i in allRating:
                    totalRate+= i.rating
                averageRate = round(totalRate/len(allRating),1)
                product = Product.objects.get(pk=request.data['product'])
                product.averageRate = averageRate
                product.save()
                response = {
                    "success":True,
                    "msg":"Create rating successfully"
                }
                return Response(response)
            response = {
                "success":False,
                "msg":"Create rating unsuccessfully"
            }
            return Response(response)

# class GetProductComment(APIView):
#     class ProductCommentSerializer(serializers.ModelSerializer):
#         class Meta:
#             model = Comment
#             fields = ['content', 'image', 'customer']

#     def get(self, request, format=None):
#         try:
#             pk = request.query_params['product']
#             page = request.query_params['page']
#             end = 5*int(page)
#             begin = end-5
#             comment = Comment.objects.filter(product=int(pk))[begin:end]
#         except Exception:
#             response = {
#                 "success":False,
#                 "msg":"Not provide productID"
#             }
#             return Response(response)
#         serializer = self.ProductCommentSerializer(comment, many=True)
#         for i in serializer.data:
#             customer = Customer.objects.get(id=i['customer'])
#             i['customer'] = {'username':customer.username, 'image':customer.image}
#             response = {
#                 "success":True,
#                 "comment":serializer.data
#             }
#         return Response(response)

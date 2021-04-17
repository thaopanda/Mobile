from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.models import update_last_login
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from django.core.validators import RegexValidator
from datetime import datetime, timedelta
from User.models import MyUser, Customer, Seller

JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

username_validator = ('^[a-zA-ZÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéêìíòóôõùúăđĩũơƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂẾưăạảấầẩẫậắằẳẵặẹẻẽềềểếỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪễệỉịọỏốồổỗộớờởỡợụủứừỬỮỰỲỴÝỶỸửữựỳỵỷỹ0-9_\s]+$')
email_validator = ('^[a-zA-Z0-9]+@[a-zA-Z.]+$')
fullname_validator = ('^[a-zA-ZÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéêìíòóôõùúăđĩũơƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂẾưăạảấầẩẫậắằẳẵặẹẻẽềềểếỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪễệỉịọỏốồổỗộớờởỡợụủứừỬỮỰỲỴÝỶỸửữựỳỵỷỹ\s]+$')
identication_validator =('^[0-9]{12}$')
phoneNumber_validator = ('^[0]{1}[0-9]{9}$')
address_validator = ('^[a-zA-ZÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéêìíòóôõùúăđĩũơƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂẾưăạảấầẩẫậắằẳẵặẹẻẽềềểếỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪễệỉịọỏốồổỗộớờởỡợụủứừỬỮỰỲỴÝỶỸửữựỳỵỷỹ0-9,\s]+$')

GENDER = [
    ('male', 'male'),
    ('female', 'female'),
    ('other', 'other'),
    ('','')
]

SHOP = [
    ("Thời trang", "Thời trang"),
    ("Công nghệ", "Công nghệ"),
    ("Trang trí", "Trang trí"),
    ("Sức khỏe và Sắc đẹp", "Sức khỏe và Sắc đẹp"),
    ("Nhà cửa và đời sống", "Nhà cửa và đời sống"),
    ("Mẹ và bé", "Mẹ và bé"),
    ("Nhà sách online", "Nhà sách online"),
    ("Ô tô - xe máy", "Ô tô - xe máy"),
    ("Thể thao du lịch", "Thể thao du lịch"),
    ("Khác", "Khác")
]

class CustomerRegistrationView(APIView):
    permission_classes = (AllowAny,)
    class CustomerRegistrationSerializer(serializers.ModelSerializer):
        username = serializers.CharField(
            max_length=30, 
            validators=[UniqueValidator(queryset=MyUser.objects.all()),
                        RegexValidator(regex=username_validator)]
        )
        email = serializers.EmailField(
            validators=[UniqueValidator(queryset=MyUser.objects.all()),
                        RegexValidator(regex=email_validator)],
            max_length=60
        )
        password = serializers.CharField(min_length=8)
        class Meta:
            model = Customer
            fields = ['id', 'email', 'username', 'password']
        
    def post(self, request, format=None):
        serializer = self.CustomerRegistrationSerializer(data=request.data)
        if(serializer.is_valid()):
            Customer.objects.create_user(email=serializer.validated_data['email'], username=serializer.validated_data['username'], password=serializer.validated_data['password'])
            response = {
                "success":True
            }
            return Response(response)

        response ={
            "success":False,
            "msg": serializer.errors
        }
        return Response(response)

class LoginView(APIView):
    permission_classes = (AllowAny,)
    class LoginViewSerializer(serializers.Serializer):
        username = serializers.CharField(read_only=True)
        email = serializers.EmailField(max_length=255)
        password = serializers.CharField(max_length=128, write_only=True, min_length=8)
        token = serializers.CharField(max_length=255, read_only=True)
        user_type = serializers.CharField(max_length=10, read_only=True)

        def validate(self, data):
            email = data.get('email', None)
            password = data.get('password', None)
            user = authenticate(email=email, password=password)
            if user is None:
                raise serializers.ValidationError("user not found")
            if(user.check_password(password) is False):
                raise serializers.ValidationError("password is incorrect")
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)
            return{
                'username':user.username,
                'email': user.email,
                'token':jwt_token,
                'user_type':user.user_type,
            }
    def post(self, request, format=None):
        serializer = self.LoginViewSerializer(data=request.data)
        if(serializer.is_valid()):
            response = {
            'success' : True,
            'username':serializer.data['username'],
            'email': serializer.data['email'],
            'token' : serializer.data['token'],
            'user_type':serializer.data['user_type']
            }
            return Response(response)
        response = {
            "success":False
        }
        return Response(response)

class SellerRegistrationView(APIView):
    permission_classes = (AllowAny,)
    class SellerRegistrationSerializer(serializers.ModelSerializer):
        email = serializers.EmailField(
            validators=[RegexValidator(regex=email_validator)]
        )
        username = serializers.CharField(
            validators=[RegexValidator(regex=username_validator)]
        )
        password = serializers.CharField(min_length=8)
        identication = serializers.CharField(
            validators=[RegexValidator(regex=identication_validator), 
                        UniqueValidator(queryset=Seller.objects.all())]
        )
        phoneNumber = serializers.CharField(
            validators=[RegexValidator(regex=phoneNumber_validator), 
                        UniqueValidator(queryset=Seller.objects.all())]
        )
        address = serializers.CharField(
            validators=[RegexValidator(regex=address_validator)]
        )
        fullname = serializers.CharField(
            validators=[RegexValidator(regex=fullname_validator)],
            max_length=50
        )
        shopName = serializers.CharField()
        shopCategory = serializers.MultipleChoiceField(choices = SHOP)
        class Meta:
            model = Seller
            fields = ['id', 'email', 'username', 'password', 'fullname', 'identication', 'address', 'phoneNumber', 'shopName', 'shopCategory']
    def post(self, request, format=None):
        serializer = self.SellerRegistrationSerializer(data=request.data)
        if(serializer.is_valid()):
            category = ','.join(map(str, serializer.validated_data['shopCategory']))

            Seller.objects.create_user(email=serializer.validated_data['email'], 
                                    username=serializer.validated_data['username'], 
                                    password=serializer.validated_data['password'], 
                                    fullname=serializer.validated_data['fullname'], 
                                    identication=serializer.validated_data['identication'], 
                                    address=serializer.validated_data['address'],
                                    phoneNumber=serializer.validated_data['phoneNumber'],
                                    shopName= serializer.validated_data['shopName'],
                                    shopCategory=category)
            response = {"success":True}
            return Response(response)
        response ={
            "success":False,
            "msg": serializer.errors
        }
        return Response(response)

class CustomerProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    
    class CustomerProfileSerializer(serializers.ModelSerializer):
        class Meta:
            model = Customer
            fields = ['username', 'email', 'date_joined', 'fullname', 'image']

    def get(self, request, format=None):
        Profile = Customer.objects.get(email=request.user.email)
        serializer = self.CustomerProfileSerializer(Profile)
        return Response(serializer.data)

class SellerProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    
    class SellerProfileSerializer(serializers.ModelSerializer):
        class Meta:
            model = Seller
            fields = ['username', 'email', 'date_joined', 'fullname', 'identication', 'address', 'phoneNumber', 'image']

    def get(self, request, format=None):
        Profile = Seller.objects.get(email=request.user.email)
        serializer = self.SellerProfileSerializer(Profile)
        return Response(serializer.data)

class CustomerUpdateProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    def put(self, request, format=None):
        customer = Customer.objects.get(email=request.user.email)
        try:
            customer.fullname = request.data['fullname']
        except Exception:
            pass

        try:
            customer.gender = request.data['gender']
        except Exception:
            pass

        try:
            customer.phone = request.data['phone']
        except Exception:
            pass
        customer.save()
        response = {
            "success":True
        }
        return Response(response)


class SellerUpdateProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    def put(self, request, format=None):
        seller = Seller.objects.get(email=request.user.email)
        try:
            seller.fullname = request.data['fullname']
        except Exception:
            pass

        try:
            seller.identication = request.data['identication']
        except Exception:
            pass

        try:
            seller.phoneNumber = request.data['phoneNumber']
        except Exception:
            pass

        try:
            seller.address = request.data['address']
        except Exception:
            pass
        seller.save()
        response = {
            "success":True
        }
        return Response(response)

class SetAvatar(APIView):
    permission_classes = (IsAuthenticated,)
    class SetAvatarSerializer(serializers.ModelSerializer):
        class Meta:
            model = MyUser
            fields = ['image']
    def put(self, request, format=None):
        user = MyUser.objects.get(email=request.user.email)
        
        serializer = self.SetAvatarSerializer(user, data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(f'ok')
        return Response(f'not ok')


class GetListSeller(APIView):
    class SellerSerializer(serializers.ModelSerializer):
        class Meta:
            model = Seller
            fields = ['shopName', 'shopCategory']
    def get(self, request, begin, end, format=None):
        sellerList = Seller.objects.filter()[begin:end]
        serializer = self.SellerSerializer(sellerList, many=True)

        return Response(serializer.data)


class ChangePassword(APIView):
    permission_classes = (IsAuthenticated,)
    class ChangePasswordSerializer(serializers.ModelSerializer):
        password = serializers.CharField(min_length=8)
        new_password = serializers.CharField(min_length=8)
        class Meta:
            model = MyUser
            fields = ['password', 'new_password']
    def put(self, request, format=None):
        user = MyUser.objects.get(email=request.user.email)
        changePassword = self.ChangePasswordSerializer(user, data=request.data)
        if(changePassword.is_valid()):
            if(user.check_password(changePassword.validated_data['password']) is False):
                response = {
                    "success":False,
                    "msg":'incorrect old password'
                }
                return Response(response)
            if(changePassword.validated_data['password']==changePassword.validated_data['new_password']):
                response = {
                    "success":False,
                    "msg":'new password must be different from old password'
                }
                return Response(response)
            user.set_password(changePassword.validated_data['new_password'])
            user.save()
            response = {
                'success':True
            }
            return Response(response)
        response = {
            'success':False
        }
        return Response(response)

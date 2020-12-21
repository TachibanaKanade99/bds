from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from rest_framework import generics, pagination, status, viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from .serializers import UserSerializer, BdsSerializer, GetImageSerializer
from .pagination import CustomPageNumber
from .models import Bds

# Create your views here.
@api_view(['POST'])
def register_user(request):
    serializer_class = UserSerializer(data=request.data)

    if serializer_class.is_valid():
        User.objects.create_user(
            # serializer_class.data['first_name'],
            # serializer_class.data['last_name'],
            # serializer_class.data['email'],
            username=serializer_class.data['username'],
            password=serializer_class.data['password'],
        )
        return Response(serializer_class.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUESTS)

@api_view(['POST'])
def login_user(request):
    # serializer_class = UserSerializer(data=request.data)

    username = request.data['username']
    password = request.data['password']
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return Response("Successful!", status=status.HTTP_200_OK)
    else:
        return Response("Failed!", status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def logout_user(request):
    permission_classes = [IsAuthenticated]
    logout(request)
    return Response("Logout Successfully!", status=status.HTTP_200_OK)


# @api_view(['POST'])
# @permission_classes((permissions.AllowAny,))
# @method_decorator(csrf_exempt, name='dispatch')

# class RegisterView(CreateAPIView):
#     serializer_class = UserSerializer
#     queryset = User.objects.all()

# class UserView(APIView):
#     def get(self, request):
#         users = User.objects.get(id=1)
#         serializer_class = UserSerializer(users)
#         return Response(serializer_class.data)

#     def post(self, request):
#         serializer_class = UserSerializer(data=request.data)

#         if serializer_class.is_valid():
#             User.objects.create_user(
#                 # serializer_class.data['first_name'],
#                 # serializer_class.data['last_name'],
#                 # serializer_class.data['email'],
#                 username=serializer_class.data['username'],
#                 password=serializer_class.data['password'],
#             )
#             return Response(serializer_class.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUESTS)

class BdsView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = BdsSerializer
    queryset = Bds.objects.all().order_by('id')
    # queryset = Bds.objects.all()
    pagination_class = CustomPageNumber

class GetImageView(viewsets.ModelViewSet):
    serializer_class = GetImageSerializer
    queryset = Bds.objects.all().filter(id=1)
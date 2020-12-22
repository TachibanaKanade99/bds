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
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from .serializers import UserSerializer, BdsSerializer, GetImageSerializer
from .pagination import CustomPageNumber
from .models import Bds


from rest_framework.authentication import SessionAuthentication, BasicAuthentication 
class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

# Create your views here.

@api_view(['GET'])
def current_user(request):
    # get current user:
    serializer = UserSerializer(request.user)
    return Response({ 'username': serializer.data.get('username') })

# class UserList(APIView):
#     permission_classes = (permissions.AllowAny,)

#     def post(self, request, format=None):
#         serializer_class = UserSerializerWithToken(data=request.data)

#         if serializer_class.is_valid():
#             serializer_class.save()
#             return Response(serializer_class.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUESTS)            

class RegisterView(APIView):
    def post(self, request):
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

# @api_view(['POST'])
# def register_user(request):
#     authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
#     serializer_class = UserSerializer(data=request.data)

#     if serializer_class.is_valid():
#         User.objects.create_user(
#             # serializer_class.data['first_name'],
#             # serializer_class.data['last_name'],
#             # serializer_class.data['email'],
#             username=serializer_class.data['username'],
#             password=serializer_class.data['password'],
#         )
#         return Response(serializer_class.data, status=status.HTTP_201_CREATED)
#     else:
#         return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUESTS)

class LoginView(APIView):
    def post(self, request):
        # serializer_class = UserSerializer(data=request.data)

        username = request.data['username']
        password = request.data['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return Response("Successful!", status=status.HTTP_200_OK)
        else:
            return Response("Failed!", status=status.HTTP_400_BAD_REQUEST)


# @api_view(['POST'])
# def login_user(request):
#     authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
#     # serializer_class = UserSerializer(data=request.data)

#     username = request.data['username']
#     password = request.data['password']
#     user = authenticate(username=username, password=password)

#     if user is not None:
#         login(request, user)
#         return Response("Successful!", status=status.HTTP_200_OK)
#     else:
#         return Response("Failed!", status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    def post(self, request):
        permission_classes = [IsAuthenticated]
        logout(request)
        return Response("Logout Successfully!", status=status.HTTP_200_OK)

# @api_view(['POST'])
# def logout_user(request):
#     permission_classes = [IsAuthenticated]
#     authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
#     logout(request)
#     return Response("Logout Successfully!", status=status.HTTP_200_OK)

class BdsView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = BdsSerializer
    queryset = Bds.objects.all().order_by('id')
    # queryset = Bds.objects.all()
    pagination_class = CustomPageNumber

class GetImageView(viewsets.ModelViewSet):
    serializer_class = GetImageSerializer
    queryset = Bds.objects.all().filter(id=1)
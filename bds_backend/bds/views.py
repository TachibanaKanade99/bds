from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Max

from rest_framework import generics, pagination, status, viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.renderers import JSONRenderer


from .serializers import UserSerializer, RealEstateDataSerializer, BdsSerializer, GetImageSerializer
from .pagination import CustomPageNumber
from .models import Bds, RealEstateData

from datetime import datetime

class CsrfExemptSessionAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

# Create your views here.

# class UserList(APIView):
#     permission_classes = (permissions.AllowAny,)

#     def post(self, request, format=None):
#         serializer_class = UserSerializerWithToken(data=request.data)

#         if serializer_class.is_valid():
#             serializer_class.save()
#             return Response(serializer_class.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUESTS)          

@api_view(['GET'])
def current_user(request):
    # get current user:
    permission_classes = [IsAuthenticated]
    serializer = UserSerializer(request.user)
    return Response({ 'username': serializer.data.get('username') })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_authentication(request):
    return Response({ 'detail': 'User is authenticated' }, status=status.HTTP_200_OK)

# @method_decorator(csrf_protect, 'dispatch')
class RegisterView(APIView):
    def post(self, request):
        serializer_class = UserSerializer(data=request.data)

        if serializer_class.is_valid():
            User.objects.create_user(
                username=serializer_class.data['username'],
                password=serializer_class.data['password'],
            )
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_class.errors, status=status.HTTP_403_FORBIDDEN)

# @method_decorator(csrf_protect, 'dispatch')
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

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response("Logout Successfully!", status=status.HTTP_200_OK)

# class FilterView(APIView):
#     # permission_classes = [IsAuthenticated]

#     def post(self, request):
#         website = request.data['website']
#         price = request.data['price']
#         rows_per_page = request.data['rowsPerPage']

#         if website is not None and price is not None:
#             results = RealEstateData.objects.filter(url__contains=website, price__lte=price).order_by('id')

#             # pagination
#             paginator = CustomPageNumber()
#             paginator.page_size = rows_per_page
#             results_page = paginator.paginate_queryset(results, request)
#             results_serializer = RealEstateDataSerializer(results_page, many=True)

#             return paginator.get_paginated_response(results_serializer.data)

class RealEstateDataView(generics.ListAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = RealEstateDataSerializer

    def get_queryset(self):
        # get query parameter:
        website = self.request.query_params.get('website', None)
        price = self.request.query_params.get('price', None)
        post_type = self.request.query_params.get('post_type', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        start_date = datetime.strptime(start_date, "%m/%d/%Y")
        end_date = datetime.strptime(end_date, "%m/%d/%Y")
        now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        min_price = price[0:price.find("-")]
        max_price = price[price.find("-")+1:]

        if max_price == "max":
            max_price = RealEstateData.objects.aggregate(Max('price'))['price__max']
        
        min_price = float(min_price)
        max_price = float(max_price)

        # Overwrite queryset with filter options:
        # if start_date == end_date and start_date == now:
        #     if post_type == "Bán đất":
        #         queryset = RealEstateData.objects.filter(url__contains=website, price__range=[min_price, max_price], post_type=post_type).order_by('id')
        #     else:
        #         queryset = RealEstateData.objects.filter(url__contains=website, price__range=[min_price, max_price], post_type__contains=post_type).order_by('id')
        # else:
        if post_type == "Bán đất":
            queryset = RealEstateData.objects.filter(url__contains=website, price__range=[min_price, max_price], post_type=post_type, posted_date__range=[start_date, end_date]).order_by('id')
        else:
            queryset = RealEstateData.objects.filter(url__contains=website, price__range=[min_price, max_price], post_type__contains=post_type, posted_date__range=[start_date, end_date]).order_by('id')
        
        return queryset

# class RealEstateDataView(viewsets.ModelViewSet):
#     # permission_classes = [IsAuthenticated]
#     serializer_class = RealEstateDataSerializer
#     # queryset = RealEstateData.objects.filter(expired_date__gt=datetime.today()).order_by('id')
#     queryset = RealEstateData.objects.all().order_by('id')
#     pagination_class = CustomPageNumber

class CountView(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        start_date = request.data['start_date']
        end_date = request.data['end_date']

        if start_date is None and end_date is None:
            return Response("Null values!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # format date:
        start_date = datetime.strptime(start_date, "%m/%d/%Y")
        end_date = datetime.strptime(end_date, "%m/%d/%Y")

        all = RealEstateData.objects.filter(posted_date__range=[start_date, end_date]).count()

        # land props:
        lands = RealEstateData.objects.filter(post_type__contains='đất', posted_date__range=[start_date, end_date]).count()
        only_land = RealEstateData.objects.filter(post_type='Bán đất', posted_date__range=[start_date, end_date]).count()
        land_in_project = RealEstateData.objects.filter(post_type='Bán đất nền dự án (đất trong dự án quy hoạch)', posted_date__range=[start_date, end_date]).count()

        houses = RealEstateData.objects.filter(post_type__contains='nhà', posted_date__range=[start_date, end_date]).count()
        villa = RealEstateData.objects.filter(post_type__contains='Bán nhà biệt thự, liền kề', posted_date__range=[start_date, end_date]).count()
        town_house = RealEstateData.objects.filter(post_type__contains='Bán nhà mặt phố', posted_date__range=[start_date, end_date]).count()
        individual_house = RealEstateData.objects.filter(post_type__contains='Bán nhà riêng', posted_date__range=[start_date, end_date]).count()
        departments = RealEstateData.objects.filter(post_type__contains='căn hộ', posted_date__range=[start_date, end_date]).count()

        farms = RealEstateData.objects.filter(post_type__contains='trang trại', posted_date__range=[start_date, end_date]).count()
        warehouses = RealEstateData.objects.filter(post_type__contains='kho, nhà xưởng', posted_date__range=[start_date, end_date]).count()
        others = RealEstateData.objects.filter(post_type__contains='khác', posted_date__range=[start_date, end_date]).count() + farms + warehouses
        belong_to_projects = RealEstateData.objects.filter(project_name__isnull=False, posted_date__range=[start_date, end_date]).count()
        has_policy = RealEstateData.objects.filter(policy__isnull=False, posted_date__range=[start_date, end_date]).count()
        new_updates = RealEstateData.objects.filter(expired_date__gt=datetime.today(), posted_date__range=[start_date, end_date]).count()
        has_furniture = RealEstateData.objects.filter(furniture__isnull=False, posted_date__range=[start_date, end_date]).count()
        counts = {
            'all': all,
            'lands': lands,
            'only_land': only_land,
            'land_in_project': land_in_project,
            'houses': houses,
            'villa': villa,
            'town_house': town_house,
            'individual_house': individual_house,
            'departments': departments,
            'others': others,
            'belong_to_projects': belong_to_projects,
            'has_policy': has_policy,
            'new_updates': new_updates,
            'has_furniture': has_furniture,
        }
        return Response(counts, status=status.HTTP_200_OK)
    
    def get(self, request):
        all = RealEstateData.objects.all().count()

        # land props:
        lands = RealEstateData.objects.filter(post_type__contains='đất').count()
        only_land = RealEstateData.objects.filter(post_type='Bán đất').count()
        land_in_project = RealEstateData.objects.filter(post_type='Bán đất nền dự án (đất trong dự án quy hoạch)').count()

        houses = RealEstateData.objects.filter(post_type__contains='nhà').count()
        villa = RealEstateData.objects.filter(post_type__contains='Bán nhà biệt thự, liền kề').count()
        town_house = RealEstateData.objects.filter(post_type__contains='Bán nhà mặt phố').count()
        individual_house = RealEstateData.objects.filter(post_type__contains='Bán nhà riêng').count()
        departments = RealEstateData.objects.filter(post_type__contains='căn hộ').count()

        farms = RealEstateData.objects.filter(post_type__contains='trang trại').count()
        warehouses = RealEstateData.objects.filter(post_type__contains='kho, nhà xưởng').count()
        others = RealEstateData.objects.filter(post_type__contains='khác').count() + farms + warehouses

        belong_to_projects = RealEstateData.objects.filter(project_name__isnull=False).count()
        has_policy = RealEstateData.objects.filter(policy__isnull=False).count()
        new_updates = RealEstateData.objects.filter(expired_date__gt=datetime.today()).count()
        has_furniture = RealEstateData.objects.filter(furniture__isnull=False).count()

        # batdongsan.com.vn
        bds_all = RealEstateData.objects.filter(url__contains='batdongsan.com.vn').count()
        bds_lands = RealEstateData.objects.filter(url__contains='batdongsan.com.vn', post_type__contains='đất').count()
        bds_houses = RealEstateData.objects.filter(url__contains='batdongsan.com.vn', post_type__contains='nhà').count()
        bds_departments = RealEstateData.objects.filter(url__contains='batdongsan.com.vn', post_type__contains='căn hộ').count()
        bds_farms = RealEstateData.objects.filter(url__contains='batdongsan.com.vn', post_type__contains='trang trại').count()
        bds_warehouses = RealEstateData.objects.filter(url__contains='batdongsan.com.vn', post_type__contains='kho, nhà xưởng').count()
        bds_others = RealEstateData.objects.filter(url__contains='batdongsan.com.vn', post_type__contains='khác').count() + bds_farms + bds_warehouses

        # homedy.com
        homedy_all = RealEstateData.objects.filter(url__contains='homedy.com').count()
        homedy_lands = RealEstateData.objects.filter(url__contains='homedy.com', post_type__contains='đất').count()
        homedy_houses = RealEstateData.objects.filter(url__contains='homedy.com', post_type__contains='nhà').count()
        homedy_departments = RealEstateData.objects.filter(url__contains='homedy.com', post_type__contains='căn hộ').count()
        homedy_farms = RealEstateData.objects.filter(url__contains='homedy.com', post_type__contains='trang trại').count()
        homedy_warehouses = RealEstateData.objects.filter(url__contains='homedy.com', post_type__contains='kho, nhà xưởng').count()
        homedy_others = RealEstateData.objects.filter(url__contains='homedy.com', post_type__contains='khác').count() + homedy_farms + homedy_warehouses

        counts = {
            'all': all,
            'lands': lands,
            'only_land': only_land,
            'land_in_project': land_in_project,
            'houses': houses,
            'villa': villa,
            'town_house': town_house,
            'individual_house': individual_house,
            'departments': departments,
            'others': others,
            'belong_to_projects': belong_to_projects,
            'has_policy': has_policy,
            'new_updates': new_updates,
            'has_furniture': has_furniture,
            # batdongsan.com.vn
            'bds_all': bds_all,
            'bds_lands': bds_lands,
            'bds_houses': bds_houses,
            'bds_departments': bds_departments,
            'bds_others': bds_others,
            # homedy.com
            'homedy_all': homedy_all,
            'homedy_lands': homedy_lands,
            'homedy_houses': homedy_houses,
            'homedy_departments': homedy_departments,
            'homedy_others': homedy_others
        }
        return Response(counts, status=status.HTTP_200_OK)

class BdsView(viewsets.ModelViewSet):
    # authentication_classes = [ CsrfExemptSessionAuthentication, BasicAuthentication ]
    # permission_classes = [IsAuthenticated]
    serializer_class = BdsSerializer
    queryset = Bds.objects.all().order_by('id')
    pagination_class = CustomPageNumber

# class GetImageView(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     serializer_class = GetImageSerializer
#     queryset = Bds.objects.all().filter(id=1)
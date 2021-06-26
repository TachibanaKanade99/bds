from django.http import HttpResponse, HttpRequest, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
# from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.db.models.aggregates import Count

from rest_framework import generics, pagination, serializers, status, viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication

from .serializers import UserSerializer, RealEstateDataSerializer, BdsSerializer, GetImageSerializer
from .pagination import CustomPageNumber
from .models import Bds, RealEstateData

from datetime import datetime

# Use joblib to load model:
from joblib import load, dump

import unidecode
import numpy as np

"""
Price predition libraries 
"""

# import FunctionTransformer from sklearn.preprocessing:
from sklearn.preprocessing import FunctionTransformer, PolynomialFeatures
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import io, base64

import sys
sys.path.append('D:\\Tuan_Minh\\bds\\price_prediction_model')
from models.prepareData import getData, preprocessData, convertData
from models.models import localOutlierFactor, linearRegressionModel, polynomialRegression, calcRMSE

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
@permission_classes([IsAuthenticated])
def current_user(request):
    # get current user:
    serializer = UserSerializer(request.user)
    response = { 
        'username': serializer.data.get('username'),
        'is_superuser': serializer.data.get('is_superuser')
    }
    return Response(response, status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_authentication(request):
    return Response({ 'detail': 'User is authenticated' }, status=status.HTTP_200_OK)

class UserLstView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.all().order_by('id')
        return queryset

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
    permission_classes = [IsAuthenticated]
    serializer_class = RealEstateDataSerializer

    def get_queryset(self):
        # get query parameter:
        website = self.request.query_params.get('website', None)
        price = self.request.query_params.get('price', None)
        post_type = self.request.query_params.get('post_type', None)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        district = self.request.query_params.get('district', None)
        ward = self.request.query_params.get('ward', None)
        street = self.request.query_params.get('street', None)

        # format start_date & end_date into datetime format:
        start_date = datetime.strptime(start_date, "%m/%d/%Y")
        end_date = datetime.strptime(end_date, "%m/%d/%Y")
        # now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        min_price = price[0:price.find("-")]
        max_price = price[price.find("-")+1:]

        if max_price == "max":
            max_price = RealEstateData.objects.aggregate(Max('price'))['price__max']
        
        min_price = float(min_price)
        max_price = float(max_price)

        # create basic query:
        queryset = RealEstateData.objects

        if website is not None:
            queryset = queryset.filter(url__contains=website)

        if post_type is not None:
            queryset = queryset.filter(post_type__exact=post_type)

        if district is not None:
            queryset = queryset.filter(district__exact=district)

        if ward is not None:
            queryset = queryset.filter(ward__exact=ward)

        if street is not None:
            queryset = queryset.filter(street__exact=street)

        # update full query:
        queryset = queryset.filter(price__range=[min_price, max_price], posted_date__range=[start_date, end_date]).order_by('id')
        
        return queryset

class CountView(APIView):
    permission_classes = [IsAuthenticated]

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

        # house props:
        houses = RealEstateData.objects.filter(post_type__contains='nhà', posted_date__range=[start_date, end_date]).count()
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
            'houses': houses,
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

        houses = RealEstateData.objects.filter(post_type__contains='nhà').count()
        departments = RealEstateData.objects.filter(post_type__contains='căn hộ').count()

        farms = RealEstateData.objects.filter(post_type__contains='trang trại').count()
        warehouses = RealEstateData.objects.filter(post_type__contains='kho, nhà xưởng').count()
        others = RealEstateData.objects.filter(post_type__contains='khác').count() + farms + warehouses

        belong_to_projects = RealEstateData.objects.filter(project_name__isnull=False).count()
        has_policy = RealEstateData.objects.filter(policy__isnull=False).count()
        new_updates = RealEstateData.objects.filter(expired_date__gt=datetime.today()).count()
        has_furniture = RealEstateData.objects.filter(furniture__isnull=False).count()

        counts = {
            'all': all,
            'lands': lands,
            'houses': houses,
            'departments': departments,
            'others': others,
            'belong_to_projects': belong_to_projects,
            'has_policy': has_policy,
            'new_updates': new_updates,
            'has_furniture': has_furniture,
        }
        return Response(counts, status=status.HTTP_200_OK)

class ChartCount(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        start_date = request.data['start_date']
        end_date = request.data['end_date']

        if start_date is None and end_date is None:
            return Response("Null values!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # format date:
        start_date = datetime.strptime(start_date, "%m/%d/%Y")
        end_date = datetime.strptime(end_date, "%m/%d/%Y")

        # batdongsan.com.vn
        bds_all = RealEstateData.objects.filter(url__contains='batdongsan.com.vn', posted_date__range=[start_date, end_date]).count()
        bds_lands = RealEstateData.objects.filter(url__contains='batdongsan.com.vn', post_type__contains='đất', posted_date__range=[start_date, end_date]).count()
        bds_houses = RealEstateData.objects.filter(url__contains='batdongsan.com.vn', post_type__contains='nhà', posted_date__range=[start_date, end_date]).count()
        bds_departments = RealEstateData.objects.filter(url__contains='batdongsan.com.vn', post_type__contains='căn hộ', posted_date__range=[start_date, end_date]).count()
        bds_farms = RealEstateData.objects.filter(url__contains='batdongsan.com.vn', post_type__contains='trang trại', posted_date__range=[start_date, end_date]).count()
        bds_warehouses = RealEstateData.objects.filter(url__contains='batdongsan.com.vn', post_type__contains='kho, nhà xưởng', posted_date__range=[start_date, end_date]).count()
        bds_others = RealEstateData.objects.filter(url__contains='batdongsan.com.vn', post_type__contains='khác', posted_date__range=[start_date, end_date]).count() + bds_farms + bds_warehouses

        # homedy.com
        homedy_all = RealEstateData.objects.filter(url__contains='homedy.com', posted_date__range=[start_date, end_date]).count()
        homedy_lands = RealEstateData.objects.filter(url__contains='homedy.com', post_type__contains='đất', posted_date__range=[start_date, end_date]).count()
        homedy_houses = RealEstateData.objects.filter(url__contains='homedy.com', post_type__contains='nhà', posted_date__range=[start_date, end_date]).count()
        homedy_departments = RealEstateData.objects.filter(url__contains='homedy.com', post_type__contains='căn hộ', posted_date__range=[start_date, end_date]).count()
        homedy_farms = RealEstateData.objects.filter(url__contains='homedy.com', post_type__contains='trang trại', posted_date__range=[start_date, end_date]).count()
        homedy_warehouses = RealEstateData.objects.filter(url__contains='homedy.com', post_type__contains='kho, nhà xưởng', posted_date__range=[start_date, end_date]).count()
        homedy_others = RealEstateData.objects.filter(url__contains='homedy.com', post_type__contains='khác', posted_date__range=[start_date, end_date]).count() + homedy_farms + homedy_warehouses

        # propzy.vn
        propzy_all = RealEstateData.objects.filter(url__contains='propzy.vn', posted_date__range=[start_date, end_date]).count()
        propzy_lands = RealEstateData.objects.filter(url__contains='propzy.vn', post_type__contains='đất', posted_date__range=[start_date, end_date]).count()
        propzy_houses = RealEstateData.objects.filter(url__contains='propzy.vn', post_type__contains='nhà', posted_date__range=[start_date, end_date]).count()
        propzy_departments = RealEstateData.objects.filter(url__contains='propzy.vn', post_type__contains='căn hộ', posted_date__range=[start_date, end_date]).count()
        propzy_farms = RealEstateData.objects.filter(url__contains='propzy.vn', post_type__contains='trang trại', posted_date__range=[start_date, end_date]).count()
        propzy_warehouses = RealEstateData.objects.filter(url__contains='propzy.vn', post_type__contains='kho, nhà xưởng', posted_date__range=[start_date, end_date]).count()
        propzy_others = RealEstateData.objects.filter(url__contains='propzy.vn', post_type__contains='khác', posted_date__range=[start_date, end_date]).count() + propzy_farms + propzy_warehouses

        counts = {
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
            'homedy_others': homedy_others,
            # propzy.vn
            'propzy_all': propzy_all,
            'propzy_lands': propzy_lands,
            'propzy_houses': propzy_houses,
            'propzy_departments': propzy_departments,
            'propzy_others': propzy_others,
        }

        return Response(counts, status=status.HTTP_200_OK)

    def get(self, request):

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

        # propzy.vn
        propzy_all = RealEstateData.objects.filter(url__contains='propzy.vn').count()
        propzy_lands = RealEstateData.objects.filter(url__contains='propzy.vn', post_type__contains='đất').count()
        propzy_houses = RealEstateData.objects.filter(url__contains='propzy.vn', post_type__contains='nhà').count()
        propzy_departments = RealEstateData.objects.filter(url__contains='propzy.vn', post_type__contains='căn hộ').count()
        propzy_farms = RealEstateData.objects.filter(url__contains='propzy.vn', post_type__contains='trang trại').count()
        propzy_warehouses = RealEstateData.objects.filter(url__contains='propzy.vn', post_type__contains='kho, nhà xưởng').count()
        propzy_others = RealEstateData.objects.filter(url__contains='propzy.vn', post_type__contains='khác').count() + propzy_farms + propzy_warehouses

        counts = {
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
            'homedy_others': homedy_others,
            # propzy.vn
            'propzy_all': propzy_all,
            'propzy_lands': propzy_lands,
            'propzy_houses': propzy_houses,
            'propzy_departments': propzy_departments,
            'propzy_others': propzy_others,
        }

        return Response(counts, status=status.HTTP_200_OK)

class PieChart(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        start_date = self.request.data['start_date']
        end_date = self.request.data['end_date']

        if start_date is None and end_date is None:
            return Response("Null values!", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # format date:
        start_date = datetime.strptime(start_date, "%m/%d/%Y")
        end_date = datetime.strptime(end_date, "%m/%d/%Y")

        # land props:
        only_lands = RealEstateData.objects.filter(post_type='Bán đất', posted_date__range=[start_date, end_date]).count()
        land_in_projects = RealEstateData.objects.filter(post_type='Bán đất nền dự án (đất trong dự án quy hoạch)', posted_date__range=[start_date, end_date]).count()

        # house props:
        villas = RealEstateData.objects.filter(post_type__contains='Bán nhà biệt thự, liền kề', posted_date__range=[start_date, end_date]).count()
        town_houses = RealEstateData.objects.filter(post_type__contains='Bán nhà mặt phố', posted_date__range=[start_date, end_date]).count()
        individual_houses = RealEstateData.objects.filter(post_type__contains='Bán nhà riêng', posted_date__range=[start_date, end_date]).count()

        result = {
            # land props:
            'only_lands': only_lands,
            'land_in_projects': land_in_projects,
            # house props:
            'villas': villas,
            'town_houses': town_houses,
            'individual_houses': individual_houses
        }

        return Response(result, status=status.HTTP_200_OK)

    def get(self, request):

        # land props:
        only_lands = RealEstateData.objects.filter(post_type='Bán đất').count()
        land_in_projects = RealEstateData.objects.filter(post_type='Bán đất nền dự án (đất trong dự án quy hoạch)').count()

        # house props:
        villas = RealEstateData.objects.filter(post_type__contains='Bán nhà biệt thự, liền kề').count()
        town_houses = RealEstateData.objects.filter(post_type__contains='Bán nhà mặt phố').count()
        individual_houses = RealEstateData.objects.filter(post_type__contains='Bán nhà riêng').count()

        result = {
            # land_props:
            'only_lands': only_lands,
            'land_in_projects': land_in_projects,
            # house props:
            'villas': villas,
            'town_houses': town_houses,
            'individual_houses': individual_houses
        }

        return Response(result, status=status.HTTP_200_OK)

def isNum(num):
    try:
        int(num)
        return True
    except ValueError:
        return False

def sortLstNumAndChar(lst):
    numbers = []
    chars = []

    for item in lst:
        if isNum(item):
            numbers.append(int(item))
        else:
            chars.append(item)

    if numbers is not None and chars is not None:
        numbers.sort(reverse=False)
        chars.sort(reverse=False)
        return list(map(str, numbers)) + chars
    else:
        return None

class WardLst(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request_page = self.request.data['request_page']
        property_type = self.request.data['property_type']
        district = self.request.data['district']
        ward_lst = []   
        
        # basic query:
        query = RealEstateData.objects.values('ward')

        if property_type is not None:
            query = query.filter(post_type__exact=property_type)
        if district is not None:
            query = query.filter(district__exact=district)

        # retrieve wards by its number depend of page request:
        query = query.exclude(ward__exact=None)

        if request_page == "predict":
            query = query.annotate(count_ward=Count('ward')).filter(count_ward__gt=40)
        
        # update full query:
        query = query.order_by('ward').distinct()

        for q in query:
            ward_lst.append(q['ward'])

        # sort ward_lst:
        ward_lst = sortLstNumAndChar(ward_lst)

        return Response(ward_lst, status=status.HTTP_200_OK)

class StreetLst(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request_page = self.request.data['request_page']
        property_type = self.request.data['property_type']
        district = self.request.data['district']
        ward = self.request.data['ward']
        street_lst = []
        
        # basic query:
        query = RealEstateData.objects.values('street')

        if property_type is not None:
            query = query.filter(post_type__exact=property_type)
        if district is not None:
            query = query.filter(district__exact=district)
        if ward is not None:
            query = query.filter(ward__exact=ward)

        # update full query:
        query = query.exclude(street__exact=None)

        if request_page == "predict":
            query = query.annotate(count_street=Count('street')).filter(count_street__gt=40)
        
        # update full query:
        query = query.order_by('street').distinct()

        for q in query:
            street_lst.append(q['street'])

        # sort street_lst:
        street_lst = sortLstNumAndChar(street_lst)

        return Response(street_lst, status=status.HTTP_200_OK)

class PricePredict(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        property_type = self.request.data['property_type']
        area = float(self.request.data['area'])
        street = self.request.data['street']
        ward = self.request.data['ward']
        district = self.request.data['district']

        # format into filename:
        property_type = unidecode.unidecode(property_type).lower().replace(" ", "")
        street = unidecode.unidecode(street).lower().replace(" ", "")
        ward = unidecode.unidecode(ward).lower().replace(" ", "")
        district = unidecode.unidecode(district).lower().replace(" ", "")
        model_name = property_type + "_" + street + "_" + ward + "_" + district

        try:
            model, degree = load('../price_prediction_model/trained/' + model_name + ".joblib")

            # transform area into 2D numpy array:
            area = np.array([area])
            area = area[:, np.newaxis]
            # scale area into log:
            area = FunctionTransformer(np.log1p).fit_transform(area)

            if degree == 1:
                predicted_price = model.predict(area)
            else:
                poly_area = PolynomialFeatures(degree).fit_transform(area)
                predicted_price = model.predict(poly_area)

            # reverse price:
            predicted_price = FunctionTransformer(np.log1p).inverse_transform(predicted_price).reshape((1,))
            predicted_price = predicted_price[0]
            predicted_price = str(predicted_price) + " billion"

            return Response(predicted_price, status=status.HTTP_200_OK)
            
        except FileNotFoundError:
            return Response("Model not found!", status=status.HTTP_200_OK)

class TrainModel(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        property_type = self.request.data['property_type']
        district = self.request.data['district']
        ward = self.request.data['ward']
        street = self.request.data['street']
        isEnableLOF = self.request.data['isEnableLOF']

        data = getData(property_type, street, ward, district)

        # Preprocess data:
        if data is not None:
            data = data[~(data['area'] < 10)]
            data = data[~(data['price'] > 200)]

            # transform data into log1p
            data['area'] = (data['area']).transform(np.log1p)
            data['price'] = (data['price']).transform(np.log1p)

            # preprocessing data:
            data = preprocessData(data)
            
            if isEnableLOF:
                # remove noise data:
                data = localOutlierFactor(data, 10)

        # Split data & Train model:
        if len(data) > 30:

            # divide data into train, validate, test data:
            train_data, test_data = train_test_split(data, test_size=0.3, random_state=4)
            test_data, validate_data = train_test_split(test_data, test_size=0.5, random_state=4)

            # Train model with train_data:
            if train_data is not None and test_data is not None and validate_data is not None:

                # Sort data by area column:
                train_data = train_data.sort_values(by=['area'])
                test_data = test_data.sort_values(by=['area'])
                validate_data = validate_data.sort_values(by=['area'])

                print("\nTrain data length: ", len(train_data))
                print("Test data length: ", len(test_data))
                print("Validate data length: ", len(validate_data))

                # Manipulate data:
                X, Y = convertData(data)
                X_train, Y_train = convertData(train_data)
                X_test, Y_test = convertData(test_data)
                X_validate, Y_validate = convertData(validate_data)

                # find model by using linear regression:
                linear_model = linearRegressionModel(X_train, Y_train)

                # find Y by using linear model predict:
                Y_train_pred = linear_model.predict(X_train)

                # calculate RMSE on linear model:
                linear_train_rmse = calcRMSE(linear_model, X_train, Y_train)
                linear_test_rmse = calcRMSE(linear_model, X_test, Y_test)

                # find model by using polynomial regression:
                poly_model, poly_model_name, degree, validate_rmse = polynomialRegression(X_train, Y_train, X_validate, Y_validate, X_test, Y_test)

                # transform X and X_test:
                polynomial_features = PolynomialFeatures(degree=degree)
                X_train_poly = polynomial_features.fit_transform(X_train)
                X_test_poly = polynomial_features.fit_transform(X_test)

                # Try predicting Y
                Y_train_poly_pred = poly_model.predict(X_train_poly)

                # calculate RMSE on poly model:
                poly_train_rmse = calcRMSE(poly_model, X_train_poly, Y_train)
                poly_test_rmse = calcRMSE(poly_model, X_test_poly, Y_test)

                # Linear score:
                linear_train_r2_score = linear_model.score(X_train, Y_train)
                print("Linear Model score on train dataset: ", linear_train_r2_score)
                linear_test_r2_score = linear_model.score(X_test, Y_test)
                print("Linear Model score on test dataset: ", linear_test_r2_score)

                # Poly score:
                poly_train_r2_score = poly_model.score(X_train_poly, Y_train)
                print("Poly Model score on train dataset: ", poly_train_r2_score)
                poly_test_r2_score = poly_model.score(X_test_poly, Y_test)
                print("Poly Model score on test dataset: ", poly_test_r2_score)

                linear_cv = np.mean(cross_val_score(linear_model, X, Y, cv=5))
                poly_cv = np.mean(cross_val_score(poly_model, X, Y, cv=5))

                if linear_cv > poly_cv and linear_test_r2_score > poly_test_r2_score:
                    best_model = linear_model
                    model_name = "Linear Regression"
                    best_degree = 1

                    # Model coefficient and intercept:
                    model_coef = linear_model.coef_
                    model_intercept = linear_model.intercept_

                    # RMSE:
                    best_train_rmse = linear_train_rmse
                    best_test_rmse = linear_test_rmse

                    # R2 score:
                    best_train_r2_score = linear_train_r2_score
                    best_test_r2_score = linear_test_r2_score

                    print("Best Model is Linear")

                    # Plot linear model:
                    plt.figure(figsize=(7, 4))
                    plt.scatter(X_train, Y_train, marker='o', color='blue', label='train_data')
                    plt.scatter(X_test, Y_test, marker='o', color='red', label='test_data')
                    plt.scatter(X_validate, Y_validate, marker='o', color='green', label='validate_data')
                    plt.plot(X_train, Y_train_pred, color='black', label='train_model')
                    plt.legend(bbox_to_anchor=(1,1), loc="upper left")
                    plt.tight_layout()
                    plt.xlabel('area')
                    plt.ylabel('price')

                else:
                    best_model = poly_model
                    model_name = poly_model_name
                    best_degree = degree

                    # Model coefficient and intercept:
                    model_coef = poly_model.coef_
                    model_intercept = poly_model.intercept_

                    # RMSE:
                    best_train_rmse = poly_train_rmse
                    best_test_rmse = poly_test_rmse

                    # R2 score:
                    best_train_r2_score = poly_train_r2_score
                    best_test_r2_score = poly_test_r2_score
                    
                    print("Best Model is Poly")

                    # Plot model:
                    plt.figure(figsize=(7, 4))
                    plt.scatter(X_train, Y_train, marker='o', color='blue', label='train_data')
                    plt.scatter(X_test, Y_test, marker='o', color='red', label='test_data')
                    plt.scatter(X_validate, Y_validate, marker='o', color='green', label='validate_data')
                    plt.plot(X_train, Y_train_poly_pred, color='black', label='train_model')
                    plt.legend(bbox_to_anchor=(1,1), loc="upper left")
                    plt.tight_layout()
                    plt.xlabel('area')
                    plt.ylabel('price')

                # Save figure and encode:
                flike = io.BytesIO()
                plt.savefig(flike, bbox_inches='tight')
                b64 = base64.b64encode(flike.getvalue()).decode()
                plt.close()

                # remove "dấu":
                property_type = unidecode.unidecode(property_type.lower().replace(" ", ""))
                street = unidecode.unidecode(street.lower().replace(" ", ""))
                ward = unidecode.unidecode(ward.lower().replace(" ", ""))
                district = unidecode.unidecode(district.lower().replace(" ", ""))
                saved_model_name = property_type + "_" + street + "_" + ward + "_" + district

                if best_test_r2_score > 0.7:
                    # Save model:
                    if saved_model_name != 'bannharieng_3/2_14_10':
                        dump((best_model, best_degree), '../price_prediction_model/trained/' + model_name + ".joblib")
                
                response = {
                    "message": "Model trained successfully!",
                    "model_name": model_name,
                    "degree": best_degree,
                    "model_coef": model_coef,
                    "model_intercept": model_intercept,
                    "train_rmse": best_train_rmse,
                    "test_rmse": best_test_rmse,
                    "train_r2_score": best_train_r2_score,
                    "test_r2_score": best_test_r2_score,
                    "figure": b64
                }

        else:
            response = {
                "message": "Data Length is empty or less than 30!",
                "model_name": "None",
                "degree": "None",
                "model_coef": "None",
                "model_intercept": "None",
                "train_rmse": "None",
                "test_rmse": "None",
                "train_r2_score": "None",
                "test_r2_score": "None",
                "figure": None
            }

        return Response(response, status=status.HTTP_200_OK)


class BdsView(viewsets.ModelViewSet):
    # authentication_classes = [ CsrfExemptSessionAuthentication, BasicAuthentication ]
    permission_classes = [IsAuthenticated]
    serializer_class = BdsSerializer
    queryset = Bds.objects.all().order_by('id')
    pagination_class = CustomPageNumber

# class GetImageView(viewsets.ModelViewSet):
#     permission_classes = [IsAuthenticated]
#     serializer_class = GetImageSerializer
#     queryset = Bds.objects.all().filter(id=1)
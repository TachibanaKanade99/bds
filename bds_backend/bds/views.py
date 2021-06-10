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
from joblib import load

import unidecode
import numpy as np

# import FunctionTransformer from sklearn.preprocessing:
from sklearn.preprocessing import FunctionTransformer, PolynomialFeatures

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

        if post_type == "Bán đất":
            queryset = RealEstateData.objects.filter(url__contains=website, price__range=[min_price, max_price], post_type=post_type, posted_date__range=[start_date, end_date]).order_by('id')
        else:
            queryset = RealEstateData.objects.filter(url__contains=website, price__range=[min_price, max_price], post_type__contains=post_type, posted_date__range=[start_date, end_date]).order_by('id')
        
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

class WardLst(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        district = self.request.data['district']
        ward_lst = []   
        
        if district is None:
            query = RealEstateData.objects.values('ward').exclude(street__exact=None, ward__exact=None, district__exact=None).annotate(count_street=Count('street')).filter(count_street__gt=40).order_by().distinct()
        else:
            query = RealEstateData.objects.values('ward').filter(district__exact=district).exclude(ward__exact=None).annotate(count_street=Count('street')).filter(count_street__gt=40).order_by().distinct()

        for q in query:
            ward_lst.append(q['ward'])

        return Response(ward_lst, status=status.HTTP_200_OK)

class StreetLst(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        ward = self.request.data['ward']
        district = self.request.data['district']
        street_lst = []
        
        if ward is None and district is None:
            query = RealEstateData.objects.values('street').exclude(street__exact=None, ward__exact=None, district__exact=None).annotate(count_street=Count('street')).filter(count_street__gt=40).order_by().distinct()
        elif ward is not None and district is None:
            query = RealEstateData.objects.values('street').filter(ward__exact=ward).exclude(street__exact=None, district__exact=None).annotate(count_street=Count('street')).filter(count_street__gt=40).order_by().distinct()
        elif ward is None and district is not None:
            query = RealEstateData.objects.values('street').filter(district__exact=district).exclude(street__exact=None, ward__exact=None).annotate(count_street=Count('street')).filter(count_street__gt=40).order_by().distinct()
        else:
            query = RealEstateData.objects.values('street').filter(ward__exact=ward, district__exact=district).exclude(street__exact=None).annotate(count_street=Count('street')).filter(count_street__gt=40).order_by().distinct()

        for q in query:
            street_lst.append(q['street'])

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
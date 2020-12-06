from django.shortcuts import render
from rest_framework import viewsets
from .serializers import BdsSerializer
from .models import Bds


# Create your views here.
# class SetPagination(PageNumberPagination):
#     page_size = 5
#     page_size_query_param = 'page_size'
#     max_page_size = 100000

class BdsView(viewsets.ModelViewSet):
    serializer_class = BdsSerializer
    # pagination_class = SetPagination
    # queryset = Bds.objects.all()[:5]
    queryset = Bds.objects.all()
from django.shortcuts import render
from rest_framework import viewsets, pagination
from .serializers import BdsSerializer
from .pagination import CustomPageNumber
from .models import Bds


# Create your views here.
# class StandardResultsSetPagination(PageNumberPagination):
#     page_size = 1
#     page_size_query_param = 'page_size'
#     max_page_size = 30000

class BdsView(viewsets.ModelViewSet):
    serializer_class = BdsSerializer
    # queryset = Bds.objects.all()[:5]
    queryset = Bds.objects.all()
    pagination_class = CustomPageNumber
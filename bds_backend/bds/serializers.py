from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Bds

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            # 'first_name',
            # 'last_name',
            # 'email',
            'username',
            'password',
        )
        
    # def create(self, validated_data):
    #     user = User(username=validated_data['username'])
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user

class GetImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bds
        fields = ('images',)

class BdsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bds
        fields = (
            'id',
            'url',
            'post_title',
            'price_unit',
            'price',
            'total_site_area',
            'property_name',
            'address_id',
            'number_of_bedrooms',
            'number_of_bathrooms',
            'project_id',
            'project_size',
            'post_author',
            'property_code',
            'full_description',
            'phone_number',
            'email',
            'property_type_id',
            'property_sub_type_id',
            'block_code',
            'block_name',
            'number_of_floors',
            'floor',
            'house_design',
            'direction',
            'building_area',
            'carpet_areas',
            'unit_of_measure_id',
            'owner_is_author',
            'owner_id',
            'longitude',
            'latitude',
            'legal_info',
            'internal_facility',
            'near_facility',
            'front_length',
            'route_length',
            'updated_datetime',
            'created_datetime',
            'expired_datetime',
            'is_called_api',
            'images',
            'city',
            'district',
            'ward_commune',
            'street',
            'match_location'
        )
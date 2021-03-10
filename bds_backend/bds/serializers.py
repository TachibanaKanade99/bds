from rest_framework import serializers
from rest_framework_jwt.settings import api_settings
from django.contrib.auth.models import User
from .models import RealEstateData, Bds

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('username')

# class UserSerializerWithToken(serializers.ModelSerializer):

#     token = serializers.SerializerMethodField()
#     password = serializers.CharField(write_only=True)

#     def get_token(self, obj):
#         jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
#         jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

#         payload = jwt_payload_handler(obj)
#         token = jwt_encode_handler(payload)
#         return token

#     def create(self, validated_data):
#         password = validated_data.pop('password', None)
#         instance = self.Meta.model(**validated_data)

#         if password is not None:
#             instance.set_password(password)
#         instance.save()
#         return instance

#     class Meta:
#         model = User
#         fields = (
#             'token',
#             'username',
#             'password',
#         )

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

class GetImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bds
        fields = ('images',)

class RealEstateDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealEstateData
        fields = (
            'id',
            'url',
            'content',
            'price',
            'area',
            'location',
            'posted_author',
            'phone',
            'posted_date',
            'expired_date',
            'item_code',
            'image_urls',
            'post_type',
            'email',
            'facade',
            'entrance',
            'orientation',
            'balcony_orientation',
            'number_of_floors',
            'number_of_bedrooms',
            'number_of_toilets',
            'furniture',
            'policy',
            'project_name',
            'street',
            'ward',
            'district',
            'province'
        )

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
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.postgres.fields.array import ArrayField

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True)

    # UserProfile will be updated automatically when there is an instance of User created
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.userprofile.save()

class Bds(models.Model):
    url = models.CharField(max_length=32767)
    post_title = models.CharField(max_length=32767,null=True)
    price_unit = models.CharField(max_length=32767,null=True)
    price = models.CharField(max_length=32767,null=True)
    total_site_area = models.CharField(max_length=32767,null=True)
    property_name = models.CharField(max_length=32767,null=True)
    address_id = models.CharField(max_length=32767)
    number_of_bedrooms = models.CharField(max_length=32767,null=True)
    number_of_bathrooms = models.CharField(max_length=32767,null=True)
    project_id = models.CharField(max_length=32767,null=True)
    project_size = models.CharField(max_length=32767,null=True)
    post_author = models.CharField(max_length=32767,null=True)
    property_code = models.CharField(max_length=32767,null=True)
    # full_description = ArrayField(models.CharField(max_length=32767,null=True))
    full_description = models.CharField(max_length=32767,null=True)
    phone_number = models.CharField(max_length=32767,null=True)
    email = models.CharField(max_length=32767,null=True)
    property_type_id = models.CharField(max_length=32767,null=True)
    property_sub_type_id = models.CharField(max_length=32767,null=True)
    block_code = models.CharField(max_length=32767,null=True)
    block_name = models.CharField(max_length=32767,null=True)
    number_of_floors = models.CharField(max_length=32767,null=True)
    floor = models.CharField(max_length=32767,null=True)
    house_design = models.CharField(max_length=32767,null=True)
    direction = models.CharField(max_length=32767,null=True)
    building_area = models.CharField(max_length=32767,null=True)
    # carpet_areas = ArrayField(models.CharField(max_length=32767,null=True))
    carpet_areas = models.CharField(max_length=32767,null=True)
    unit_of_measure_id = models.CharField(max_length=32767,null=True)
    # owner_is_author = models.BooleanField(default=False)
    owner_is_author = models.CharField(max_length=32767,null=True)
    owner_id = models.CharField(max_length=32767,null=True)
    # longitude = models.DecimalField(max_digits = 30, decimal_places = 15)
    longitude = models.CharField(max_length=32767,null=True)
    # latitude = models.DecimalField(max_digits = 30, decimal_places = 15)
    latitude = models.CharField(max_length=32767,null=True)
    legal_info = models.CharField(max_length=32767,null=True)
    # internal_facility = ArrayField(models.CharField(max_length=32767,null=True))
    internal_facility = models.CharField(max_length=32767,null=True)
    # near_facility = ArrayField(models.CharField(max_length=32767,null=True))
    near_facility = models.CharField(max_length=32767,null=True)
    front_length = models.CharField(max_length=32767,null=True)
    route_length = models.CharField(max_length=32767,null=True)
    # updated_datetime = models.DateTimeField()
    # created_datetime = models.DateTimeField()
    # expired_datetime = models.DateTimeField()
    updated_datetime = models.CharField(max_length=32767,null=True)
    created_datetime = models.CharField(max_length=32767,null=True)
    expired_datetime = models.CharField(max_length=32767,null=True)
    # is_called_api = models.BooleanField(default=False)
    is_called_api = models.CharField(max_length=32767,null=True)
    images = models.CharField(max_length=32767,null=True)
    city = models.CharField(max_length=32767,null=True)
    district = models.CharField(max_length=32767,null=True)
    ward_commune = models.CharField(max_length=32767,null=True)
    street = models.CharField(max_length=32767,null=True)
    match_location = models.CharField(max_length=32767,null=True)


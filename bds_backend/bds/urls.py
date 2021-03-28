from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from .views import current_user, check_authentication, BdsView, RegisterView, LoginView, LogoutView, RealEstateDataView, CountView

# router = routers.DefaultRouter()
# router.register(r'realestatedata', RealEstateDataView, 'realestatedata')
# router.register(r'bdss', BdsView, 'bds')
# router.register(r'image', GetImageView, 'bds_image')

urlpatterns = [
    # path('api/', include(router.urls)),
    path('current_user/', current_user),
    path('check_authentication/', check_authentication),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),

    path('api/realestatedata/count/', CountView.as_view()),
    path('api/realestatedata/', RealEstateDataView.as_view())
    # path('register/', register_user),
    # path('login/', login_user),
    # path('logout/', logout_user),
]
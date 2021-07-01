from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from .views import current_user, check_authentication, BdsView, RegisterView, LoginView, LogoutView, RealEstateDataView, CountView, ChartCount, PieChart, WardLst, StreetLst, PricePredict, UserLstView, TrainModel

# router = routers.DefaultRouter()
# router.register(r'realestatedata', RealEstateDataView, 'realestatedata')
# router.register(r'bdss', BdsView, 'bds')
# router.register(r'image', GetImageView, 'bds_image')

urlpatterns = [
    # path('api/', include(router.urls)),
    path('api/current_user/', current_user),
    path('api/check_authentication/', check_authentication),
    path('api/register/', RegisterView.as_view()),
    path('api/login/', LoginView.as_view()),
    path('api/logout/', LogoutView.as_view()),

    path('api/user_lst/', UserLstView.as_view()),

    path('api/realestatedata/', RealEstateDataView.as_view()),
    path('api/realestatedata/count/', CountView.as_view()),
    path('api/realestatedata/chart_count/', ChartCount.as_view()),
    path('api/realestatedata/piechart_count/', PieChart.as_view()),
    path('api/realestatedata/ward_lst/', WardLst.as_view()),
    path('api/realestatedata/street_lst/', StreetLst.as_view()),
    path('api/realestatedata/price_predict/', PricePredict.as_view()),
    path('api/realestatedata/train_model/', TrainModel.as_view()),
    # path('register/', register_user),
    # path('login/', login_user),
    # path('logout/', logout_user),
]
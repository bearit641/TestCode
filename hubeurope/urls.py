from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.urls import include

from .views import DashboardBaseTemplateView
from .views import FrontPageBaseTemplateView


# Used by apps implementing API endpoints
router = routers.DefaultRouter()

api_v1_urlpatterns = [
    path('auth/token/', obtain_auth_token),
    path(r'', include('hubcommon.urls')),
    path(r'', include('tracking.urls')),
    path(r'', include(router.urls))
]

urlpatterns = [

    path('charts/', DashboardBaseTemplateView.as_view(), name='dashboard_charts'),

    path('', FrontPageBaseTemplateView.as_view(), name='front_page'),

    path('admin/', admin.site.urls),

    path('accounts/', include('django.contrib.auth.urls')),

    path('billing/', include('invoicing.urls', namespace='invoicing')),

    path(
        'charts/',
        include('charts.urls', namespace='charts')
    ),

    path(
        'clients/',
        include('clients.urls', namespace='clients')
    ),

    path(
        'labels/',
        include('despatch_cloud.urls', namespace='despatch_cloud')
    ),

    path(
        'gardening-direct-records/',
        include('gardening_direct.urls', namespace='gardening_direct')
    ),

    path(
        'mobile-integrations/',
        include('mobile_integrations.urls', namespace='mobile_integrations')
    ),

    path(
        'scanner/',
        include('scanner.urls', namespace='scanner')
    ),

    path(
        'services/',
        include('services.urls', namespace='services')
    ),

    path(
        'signup/',
        include('signup.urls', namespace='signup')
    ),

    path('surcharges/', include('surcharges.urls', namespace='surcharges')),

    path(
        'unbilled_parcel/',
        include('unbilled_parcel.urls', namespace='unbilled_parcel')
    ),

    path(
        'users/',
        include('users.urls', namespace='users')
    ),

    path(
        'parcel-cost/',
        include('parcel_costs.urls', namespace='parcel_costs')
    ),

    path(
        'parcel/subscriptions/',
        include('parcel_subscriptions.urls', namespace='parcel_subscriptions')
    ),

    url(r'^api/v1/', include((api_v1_urlpatterns, 'api_v1'), namespace='v1')),
]

handler404 = 'hubeurope.views.handler404'
handler500 = 'hubeurope.views.handler500'

from django.urls import path
from zkapi.views import *


urlpatterns = [
    path('attendance/today/', AttendanceAPIView.as_view(), name='today-attendance'),
    path('devices/', DeviceListCreateAPIView.as_view(), name='device-list-create'),
    path('devices/<uuid:pk>/', DeviceRetrieveUpdateDestroyAPIView.as_view(), name='device-detail'),
]
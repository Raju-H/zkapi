from django.urls import path
from accounts.views import *
from .views import *


urlpatterns = [
    path('login/', LoginAPI.as_view(), name='login'),
    path("register/", RegisterAPI.as_view(), name="register"),
    path("verify/", VerifyOTP.as_view(), name="verify"),
    path("password-reset/request/", PasswordResetRequestAPI.as_view(), name="password-reset-request"),
    path("password-reset/", PasswordResetAPI.as_view(), name="password-reset"),
]


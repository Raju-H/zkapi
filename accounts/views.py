from .models import User
from .serializers import *
from .emails import *


import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.tokens import RefreshToken


class LoginAPI(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            try:
                user = User.objects.get(email=email)
                
                if not user.check_password(password):
                    return Response({
                        'status': 400,
                        'message': 'Invalid credentials: Incorrect password',
                    }, status=status.HTTP_400_BAD_REQUEST)

                if not user.is_verified:
                    return Response({
                        'status': 400,
                        'message': 'Email not verified',
                    }, status=status.HTTP_400_BAD_REQUEST)

                refresh = RefreshToken.for_user(user)
                
                return Response({
                    'status': 200,
                    'message': 'Login successful',
                    'data': {
                        'email': user.email,
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                }, status=status.HTTP_200_OK)

            except ObjectDoesNotExist:
                return Response({
                    'status': 404,
                    'message': 'Invalid credentials: Email not found',
                }, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'status': 400,
            'message': 'Invalid data',
            'errors': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)




class RegisterAPI(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.create(serializer.validated_data)
            
            user.set_password(serializer.validated_data['password'])
            user.otp = random.randint(1000, 9999)
            user.save()
            
            send_otp_via_email(user.email, user.otp)
            
            return Response({
                'status': 200,
                'message': 'User created successfully. Check your email for OTP verification.',
                'data': {'email': user.email},
            }, status=status.HTTP_201_CREATED)

        return Response({
            'status': 400,
            'message': 'Something went wrong',
            'data': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTP(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            try:
                user = User.objects.get(email=email)
                if user.otp == otp:
                    user.is_verified = True
                    user.otp = None
                    user.save()
                    return Response({
                        'status': 200,
                        'message': 'User verified successfully.',
                    }, status=status.HTTP_200_OK)
                else:
                    return Response({
                        'status': 400,
                        'message': 'Invalid OTP.',
                    }, status=status.HTTP_400_BAD_REQUEST)
            except ObjectDoesNotExist:
                return Response({
                    'status': 404,
                    'message': 'Email not found.',
                }, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'status': 400,
            'message': 'Invalid data.',
            'errors': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)
    


class PasswordResetRequestAPI(APIView):
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                send_password_reset_email(email)
                return Response({
                    'status': 200,
                    'message': 'Password reset email sent.',
                }, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({
                    'status': 404,
                    'message': 'Email not found.',
                }, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'status': 400,
            'message': 'Invalid data.',
            'errors': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)
    


class PasswordResetAPI(APIView):
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']

            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                email = payload['email']
                
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()

                return Response({
                    'status': 200,
                    'message': 'Password has been reset successfully.',
                }, status=status.HTTP_200_OK)

            except jwt.ExpiredSignatureError:
                return Response({
                    'status': 400,
                    'message': 'The token has expired.',
                }, status=status.HTTP_400_BAD_REQUEST)
            except jwt.InvalidTokenError:
                return Response({
                    'status': 400,
                    'message': 'Invalid token.',
                }, status=status.HTTP_400_BAD_REQUEST)
            except ObjectDoesNotExist:
                return Response({
                    'status': 404,
                    'message': 'Email not found.',
                }, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'status': 400,
            'message': 'Invalid data.',
            'errors': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from kavenegar import KavenegarAPI, APIException, HTTPException

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from kavenegarapp.models import OTPRequest
from kavenegarapp import serializers

from django.contrib.auth import get_user_model


class OTPView(APIView):
    def get(self, request):
        serializer = serializers.RequestOTPSerializer(data=request.query_params)
        if serializer.is_valid():
            data = serializer.validated_data
            try:
                otp = OTPRequest.objects.generate(data)
                return Response(data=serializers.RequestOTPResponseSerializer(otp).data)
            except Exception as e:
                print (e)
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=serializer.errors)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
    def post(self, request):
        serializer = serializers.VerifyOtpRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            if OTPRequest.objects.is_valid(data['receiver'],data['request_id'], data['password']):
                return Response(self._handle_login(data))
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

    def _handle_login(self, otp):
        User = get_user_model()

        query = User.objects.filter(phone_number=otp['receiver'])

        if query.exists():
            created = False
            user = query.first()
        else:
            user = User.objects.create(phone_number=otp['receiver'])
            created = True
        
        refresh = RefreshToken.for_user(user)

        return serializers.ObtainTokenSerializer({
            'refresh': str(refresh),
            'token': str(refresh.access_token),
            'created': created
        }).data

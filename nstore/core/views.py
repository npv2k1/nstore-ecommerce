
import requests
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.encoding import (DjangoUnicodeDecodeError, force_str,
                                   smart_bytes, smart_str)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from nstore.core.serializers import ChangePasswordSerializer
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.response import Response
# Create your views here.
from rest_framework.views import APIView

from .models import User
from .serializers import ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer
from .utils import Util

# @api_view(["GET"])
# @permission_classes([permissions.AllowAny])
# def UserActivationView(request, uid, token):
#     # protocol = 'https://' if request.is_secure() else 'http://'
#     # web_url = protocol + request.get_host()
#     # post_url = web_url + "/auth/users/activate/"
#     # post_data = {'uid': uid, 'token': token}
#     # result = requests.post(post_url, data=post_data)
#     # content = result.text
#     return Response("Hello")
import os
from django.http import HttpResponsePermanentRedirect


class CustomRedirect(HttpResponsePermanentRedirect):

    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RequestPasswordResetEmail(GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer
    def post(self, request):
        email = request.data.get('email', '')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            token = PasswordResetTokenGenerator().make_token(user)
            email_body = 'Hello, \n Use link below to reset your password  \n' + token

            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
            Util.send_email(data)
            return Response({'success': 'We have sent you a link to reset your password'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)


class PasswordTokenCheckAPI(GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def post(self, request, *args, **kwargs):

        email = request.data.get('email', '')
        token = request.data.get('token', '')

        try:

            user = get_object_or_404(User, email=email)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'success': 'Token is valid'}, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)

            except UnboundLocalError as e:
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordAPIView(GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)

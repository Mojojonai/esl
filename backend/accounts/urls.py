from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from .models import UserProfile
from .serializers import ChangePasswordSerializer
from rest_framework.authtoken.models import Token


class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {'detail': 'Username and password are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {'detail': 'Invalid credentials.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if not user.check_password(password):
            return Response(
                {'detail': 'Invalid credentials.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        token, _ = Token.objects.get_or_create(user=user)
        
        profile_data = {}
        if hasattr(user, 'profile'):
            profile = user.profile
            profile_data = {
                'current_level': profile.current_level,
                'current_unit': profile.current_unit,
                'xp': profile.xp,
                'streak': profile.streak,
                'first_login': profile.first_login,
                'password_changed': profile.password_changed,
            }
        
        return Response({
            'token': token.key,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_staff': user.is_staff,
            },
            'profile': profile_data,
        })


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            new_password = serializer.validated_data['new_password']
            old_password = serializer.validated_data.get('old_password', '')

            if hasattr(user, 'profile') and user.profile.password_changed:
                if not user.check_password(old_password):
                    return Response(
                        {'old_password': 'Old password is incorrect.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            user.set_password(new_password)
            user.save()

            if hasattr(user, 'profile'):
                profile = user.profile
                profile.password_changed = True
                profile.first_login = False
                profile.save()

            return Response({'detail': 'Password changed successfully.'})

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({'detail': 'Logged out successfully.'})


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('token/', obtain_auth_token, name='api_token_auth'),
]

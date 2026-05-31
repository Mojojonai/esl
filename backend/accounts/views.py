from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import UserProfile
from .serializers import (
    UserSerializer, UserProfileSerializer, UserDetailSerializer,
    ChangePasswordSerializer
)


class IsAdminOrOwner(permissions.BasePermission):
    """
    Permission class that allows admin or the user themselves to access.
    """
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True
        return obj.user == request.user if hasattr(obj, 'user') else obj == request.user


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User management.
    """
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user profile."""
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def change_password(self, request, pk=None):
        """Change user password."""
        user = self.get_object()
        
        if user != request.user and not request.user.is_staff:
            return Response(
                {'detail': 'You do not have permission to change this password.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']
            old_password = serializer.validated_data.get('old_password', '')

            if user == request.user and hasattr(user, 'profile') and user.profile.password_changed:
                if not old_password or not user.check_password(old_password):
                    return Response(
                        {'old_password': 'Old password is incorrect.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
            
            user.set_password(new_password)
            user.save()
            
            # Mark password as changed if first login
            if hasattr(user, 'profile'):
                profile = user.profile
                profile.password_changed = True
                profile.first_login = False
                profile.save()
            
            return Response({'detail': 'Password changed successfully.'})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for UserProfile management.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrOwner]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return UserProfile.objects.all()
        return UserProfile.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        """Get current user's profile."""
        profile = request.user.profile
        serializer = self.get_serializer(profile)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def update_level(self, request):
        """Update user's current level."""
        profile = request.user.profile
        new_level = request.data.get('level')
        
        valid_levels = ['A1', 'A2', 'B1', 'B2', 'C1']
        if new_level not in valid_levels:
            return Response(
                {'detail': 'Invalid level.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        profile.current_level = new_level
        profile.save()
        
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

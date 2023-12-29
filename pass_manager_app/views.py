from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from pass_manager_app import serializers
from . import models
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from . import permissions
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class HelloApiView(APIView): 
    """test API View"""
    
    serializer_class = serializers.HelloSerializer
    
    
    def get(self, request, format=None):
        """returns a list of APIView Features"""
        
        an_apiview = [
            'Uses HTTP methods as functions (get, post, patch, put, delete)', 
            'Is similar to a traditional Django View', 
            'Gives you the most contorl over your application logic', 
            'Is mapped manaully to URLs', 
        ]
        
        return Response({'Message': 'Hello', 'an_apiview': an_apiview })
    
    def post(self, request): 
        """Create a hello message with our name"""
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message': message})
        else: 
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
                )
            
            
    def put(self, request, pk=None): 
        """Handle updating an object"""
        return Response({'method': 'PUT'})
    
    def patch(self, request, pk=None): 
        """Handle a partial update of an object"""
        return Response({'method': 'PATCH'})
    
    def delete(self, request, pk=None):
        """Delete an object"""
        return Response({'method':'DELETE'})
         
         
class HelloViewSet(viewsets.ViewSet): 
    """Test API ViewSet"""
    serializer_class = serializers.HelloSerializer
    def list(self, request):
        """Return a hello message"""
        
        a_viewset = [
            'Uses actions (list, create, retrieve, update, partial updates)', 
            'Automatically maps to URLs using Routers', 
            'Provides more functionality with less code'
        ]     

        return Response({'message': 'Hello', 'a_viewset': a_viewset})
    
    def create(self, request):
        """create a new hello message"""
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid(): 
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({'message': message})
        else: 
            return Response(
                serializer.errors, 
                status=status.HTTP_400_BAD_REQUEST
            )        
            
    def retrieve(self, request, pk=None):
        """"Handle getting an object by its ID """
        return Response({'http_method': "GET"})
    
    def update(self, request, pk=None): 
        """"Handle updating an ohject"""
        return Response({'http_method': 'PUT'})
    
    def partial_update(self, request, pk=None):
        """Handle updating part of an object"""
        return Response({'http_method': 'PATCH'})
    
    def destroy(self, request, pk=None):
        """Handle removing an object"""
        return Response({'http_method': 'DESTROY'})
    
class UserProfileViewSet(viewsets.ModelViewSet):
    """Handles creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.UpdateOwnProfile, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', 'email', )
    
    
class UserLoginApiView(ObtainAuthToken): 
    """Handle Creating user authintication tokens"""
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
       

class UserProfileFeedViewSet(viewsets.ModelViewSet): 
    """Handles Creating, reading, and updating profile feed items"""
    authentication_classes = (TokenAuthentication, )
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (
        permissions.UpdateOwnStatus, 
        IsAuthenticated
    )
    
    def perform_create(self, serializer):
        """Sets the user profile to the loged in user"""
        serializer.save(user_profile=self.request.user)
    
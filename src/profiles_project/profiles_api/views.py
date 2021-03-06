from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# import viewsets
from rest_framework import viewsets
# import status
from rest_framework import status

# import our serializer object
from . import serializers

# import models
from . import models

# import permissions
from . import permissions

# import token auth
from rest_framework.authentication import TokenAuthentication

# import filter model
from rest_framework import filters

from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
# if a user is Authenticated, he can do anything
# if not, he can only readonly
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated


# Create your views here.

class HelloApiView(APIView):
    """Test API View."""
    # Tells the django rest framework that the serializer class
    # for this APIView
    serializer_class = serializers.HelloSerializer


    def get(self, request, format=None):
        """Returns a list of APIView features."""

        # Some features an api view provides
        an_apiview = [
            'Uses HTTP methods as function (get, post, patch, put, delete)',
            'It is similar to a tranditional Django view',
            'Gives you the most control over your logic',
            'It mapped manually to URLs'
        ]

        # return this list in a response object
        # so it can be output from the API
        # A response object must be passed a dictionary to return the response
        return Response({'message':'Hello!', 'an_apiview':an_apiview})

        # return a message that includes the naem that was posted to the API
    def post(self, request):
        """Create a hello message with our name."""
        serializer = serializers.HelloSerializer(data=request.data)

        # check the serializer has valid data passed into
        if serializer.is_valid():
            name = serializer.data.get('name')
            # Create a string and in the string, we pass in the name using
            # the format function of the string
            # if you want to insert mul different items in the
            # string you would use these curly brackets and use the order
            # that you want them to go in
            message = 'Hello {0}'.format(name)
            return Response({'message': message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Handles updating an object."""

        return Response({'method': 'put'})

    def patch(self, request, pk=None):
        """Patch request, only updates fields provided in the request."""

        return Response({'method': 'patch'})

    def delete(self, request, pk=None):
        """Deletes and object."""

        return Response({'method': 'delete'})

class HelloViewSet(viewsets.ViewSet):
    """Test API viewset. """
    serializer_class = serializers.HelloSerializer

    # Add LIST action
    # list all of the objects in the system
    def list(self, request):
        """Return a hello message. """
        a_viewset = [
            'Uses actions(list, retrieve, updates, partial_update)',
            'Automatically maps to URLs using Routers',
            'Provides more functionality with less code'
        ]

        return Response({'message':'Hello!', 'a_viewset': a_viewset})

    # Add CREATE action
    # the create function take care of the HTTP POST
    # function; Create a new object in the system
    def create(self, request):
        """ create a new hello message. """

        # define the serializer, and pass it the request data
        serializer = serializer.HelloSerializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message':message})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Add retrieve action
    # It takes care of getting a specifit object by its id
    def retrieve(self, request, pk=None):
        """Handles getting an object by its ID"""

        return Response({'http_method': 'GET'})

    # Add UPDATE action
    # the create function take care of the HTTP PUT
    # function; update an object in the system
    def update(self, request, pk=None):
        """Handles updating an object by its ID"""
        return Response({'http_method': 'PUT'})

    # Add PARTIAL UPDATING action
    # the create function take care of the HTTP Patch
    # function; partial update an object in the system
    def partial_update(self, request, pk=None):
        """Handles partial updating an object by its ID"""
        return Response({'http_method': 'PATCH'})

    # Add DESTORY action
    # the create function take care of the HTTP DELETE
    # function; delete an object in the system
    def destroy(self, request, pk=None):
        """Handles removing an object by its ID"""
        return Response({'http_method': 'DELETE'})

class UserProfileViewSet(viewsets.ModelViewSet):
    """Handls creating, reading and updating profiles. """

    # define the serializer class
    # the serializer has the model class set in the
    # Metadata, it knows which model to look for handling out user obj
    serializer_class = serializers.UserProfileSerializer

    # Create the query set, which tells the viewset
    # how to retrieve the object from our db.
    # list all objects in the db
    queryset = models.UserProfile.objects.all()

    # Adding token authentication, tuple lists what type of auth
    authentication_classes = (TokenAuthentication,)

    # Defining the permission class, tuple
    permission_classes = (permissions.UpdateOwnProfile,)

    # list all filters we want in the tuple have as an option on this viewset
    filter_backends = (filters.SearchFilter,)

    # we need to tell it which fields we want to allow the user to filter by
    # name and email are the fields that we want to search on
    search_fields = ('name', 'email',)

class LoginViewSet(viewsets.ViewSet):
    """Checks email and password and returns an auth token. """
    # Set the serializer class to the auth token serializer
    serializer_class = AuthTokenSerializer

    # Define a create function
    # create is what is called when you make a HTTP POST to the viewset
    def create(self, request):
        """Use the ObtainAuthToken APIView to validate and create a token. """
        # pass the request through to the ObtainAuthToken API view
        # and call the post function
        return ObtainAuthToken().post(request)

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating, reading and updating feed items. """

    # Adding token authentication, tuple lists what type of auth
    authentication_classes = (TokenAuthentication,)

    # define the serializer class
    # the serializer has the model class set in the
    # Metadata, it knows which model to look for handling out user obj
    serializer_class = serializers.ProfileFeedItemSerializer

    # Create the query set, which tells the viewset
    # how to retrieve the object from our db.
    # list all objects in the db
    queryset = models.ProfileFeedItem.objects.all()
    # It will only allow them to update and create and modify
    # if they log in,  or it will restrict them to read_only
    # And then, if the user is trying to create or update a new status
    # it will run our permissions.PostOwnStatus to check whether they
    # try to update their own status.
    permission_classes = (permissions.PostOwnStatus, IsAuthenticated)

    # the perform_create function is a func that we can add
    # to our viewset to customize the logic that's run when
    # we create a new object for our viewset.
    # when django rest framework creates a new object in our viewset
    # we want to customize this to make sure that the user profile
    # of the ProfileFeedItem is set to the currently logined in user.
    # When the rest framework creates a new object  with our
    # vewset it will call this function and it will pass
    # on the valid serializer
    # we can then use the serializer to create a new object
    # but when we create a new object, we will manually set
    # the user profile to the profile that is currently
    # logged in.
    def perform_create(self, serializer):
        """Sets the user profile to the logged in user. """
        serializer.save(user_profile=self.request.user)

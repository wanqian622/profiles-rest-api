from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# import status
from rest_framework import status

# import our serializer object
from . import serializers


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

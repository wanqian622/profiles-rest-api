from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.

class HelloApiView(APIView):
    """Test API View."""


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

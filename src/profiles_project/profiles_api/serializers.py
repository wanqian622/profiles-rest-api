from rest_framework import serializers
from . import models

class HelloSerializer(serializers.Serializer):
    """ Serialize a name field for testing our APIViews."""
    name = serializers.CharField(max_length=10)


class UserProfileSerializer(serializers.ModelSerializer):
    """A serializer for our user profile object. """

    class Meta:
        # Assigning the model that the meta class points to
        # this model serializer is going to be used
        # with our user profile model
        model = models.UserProfile

        # What field in our model we want to use in this serializer
        fields = ('id', 'email', 'name', 'password')

        # Define some extra keyword arguments for our model
        # Tells django rest framework special attributes that
        # we want to apply to this fields
        # password: write only
        # key in extra_kwargs dic corresponds to which specfic
        # field we want to add special keyword
        extra_kwargs = {'password': {'write_only': True}}


    # create a special function that overrides the create
    # functionality
    # Encrypt password
    def create(self, validated_data):
        """ Create and return a new user. """
        # use validated_data to create our new user object.
        # create a new user model object
        user = models.UserProfile(
            email=validated_data['email'],
            name=validated_data['name']
        )
        user.set_password(validated_data['password'])

        # save the user object into db
        user.save()

        return user

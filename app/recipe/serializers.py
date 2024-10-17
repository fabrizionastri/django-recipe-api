""" Serializers for recipe app """

from rest_framework import serializers

from core.models import Recipe

class RecipeSerializer(serializers.ModelSerializer):
    """ Serializer for the recipe. """

    class Meta:
        model = Recipe
        # fields = '__all__'               # this is a shortcut to include all fields in the model
        fields = ('id', 'title', 'time_minutes', 'price', 'link')
        read_only_fields = ('id',)
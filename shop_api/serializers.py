from rest_framework import serializers

from shop_api.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for the Category model.
    Converts Category model instances to JSON format and vice versa.
    """

    class Meta:
        """
        Meta class to specify the model and fields to be used in the serializer.
        """

        model = Category
        fields = "__all__"

"""Serializers."""

from rest_framework import serializers

from .models import Category, Product, Review, Supplier

ALL = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.

    Fields:
        owner: Read-only field displaying the username of the product's owner.
    """

    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        """
        Meta options for the ProductSerializer.

        Attributes:
            model: The model that is being serialized.
            fields: The fields to be included in the serialization.
            read_only_fields: The fields that are read-only.
        """

        model = Product
        fields = ALL
        read_only_fields = ['owner']


class SupplierSerializer(serializers.ModelSerializer):
    """
    Serializer for the Supplier model.

    Fields:
        owner: Read-only field displaying the username of the supplier's owner.
    """

    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        """
        Meta options for the SupplierSerializer.

        Attributes:
            model: The model that is being serialized.
            fields: The fields to be included in the serialization.
            read_only_fields: The fields that are read-only.
        """

        model = Supplier
        fields = ALL
        read_only_fields = ['owner']


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model.

    Fields:
        owner: Read-only field displaying the username of the review's owner.
    """

    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        """
        Meta options for the ReviewSerializer.

        Attributes:
            model: The model that is being serialized.
            fields: The fields to be included in the serialization.
            read_only_fields: The fields that are read-only.
        """

        model = Review
        fields = ALL
        read_only_fields = ['owner']


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for the Category model."""

    class Meta:
        """
        Meta options for the CategorySerializer.

        Attributes:
            model: The model that is being serialized.
            fields: The fields to be included in the serialization.
        """

        model = Category
        fields = ALL

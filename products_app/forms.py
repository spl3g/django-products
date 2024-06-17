"""Forms."""

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import CharField, HiddenInput, ModelForm

from .models import Product, Review, Supplier

REGISTER_CHAR_LEN = 100


def validate_username(username):
    """
    Validate that the provided username so is not already in use.

    Args:
        username (str): The username to validate.

    Raises:
        ValidationError: If the username is already in use.
    """
    if User.objects.filter(username=username).exists():
        raise ValidationError(f'The username "{username}" is already in use.')


class RegistrationForm(UserCreationForm):
    """
    A form for user registration that extends Django's UserCreationForm.

    Fields:
        username: The username of the user.
        password1: The user's password.
        password2: Confirmation of the user's password.
    """

    class Meta:
        """Meta."""

        model = User
        fields = ['username', 'password1', 'password2']


class ReviewCreationForm(ModelForm):
    """
    A form for creating a review for a product.

    Fields:
        text: The text content of the review.
        rating: The rating given in the review.
        product_id: The ID of the product being reviewed, hidden from the user.
    """

    product_id = CharField(widget=HiddenInput())

    class Meta:
        """Metadata."""

        model = Review
        fields = ('text', 'rating')


class ProductCreationForm(ModelForm):
    """
    A form for creating a product.

    Fields:
        name: The name of the product.
        price: The price of the product.
        category: The category of the product.
        supplier: The supplier of the product, hidden from the user.
    """

    supplier = CharField(widget=HiddenInput())

    class Meta:
        """Meta."""

        model = Product
        fields = ('name', 'price', 'category')


class SupplierRegistrationForm(ModelForm):
    """
    A form for registering a new supplier.

    Fields:
        name: The name of the supplier.
        phone: The phone number of the supplier.

    Labels:
        name: Custom label for the name field.
        phone: Custom label for the phone field.
    """

    class Meta:
        """Meta."""

        model = Supplier
        fields = ('name', 'phone')

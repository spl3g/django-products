"""Models."""

import re
from uuid import uuid4

from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class UUIDMixin(models.Model):
    """Abstract model mixin that adds a UUID primary key to a model."""

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        """Metadata."""

        abstract = True


class OwnerMixin(models.Model):
    """
    Abstract model mixin that adds an owner field to a model.

    The owner is a foreign key to the User model.
    """

    owner = models.ForeignKey(
        'auth.User', related_name='%(class)s', on_delete=models.CASCADE)

    class Meta:
        """Metadata."""

        abstract = True


class PositiveDecimalField(models.DecimalField):
    """Custom DecimalField that ensures positive values."""

    def formfield(self, **kwargs):
        """
        Customize the form field to enforce a minimum value of 0.

        Args:
            kwargs: keword arguments

        Returns:
            formfield: super formfield
        """
        return super().formfield(
            **{
                'min_value': 0,
                'max_digits': self.max_digits,
                'decimal_places': self.decimal_places,
                'form_class': forms.DecimalField,
                **kwargs,
            },
        )


SHORT_TEXT_MAX = 100
LONG_TEXT_MAX = 1000


class Category(UUIDMixin):
    """
    Model representing a product category.

    Fields:
        name: The name of the category.
        description: A description of the category.
    """

    name = models.TextField(max_length=SHORT_TEXT_MAX)
    description = models.TextField(max_length=LONG_TEXT_MAX, blank=True)

    def __str__(self) -> str:
        """
        Return self name.

        Returns:
            name (str): name
        """
        return f'{self.name}'

    class Meta:
        """Metadata."""

        verbose_name_plural = _('categories')
        ordering = ['name']


def check_positive(num: int) -> None:
    """
    Validate that ensuresnsure a number is positive.

    Args:
        num (int): The number to check.

    Raises:
        ValidationError: If the number is not positive.
    """
    if num < 0:
        raise ValidationError('price should be bigger than zero')


class Product(UUIDMixin, OwnerMixin):
    """
    Model representing a product.

    Fields:
        name: The name of the product.
        category: The category the product belongs to.
        supplier: The supplier of the product.
        price: The price of the product.
    """

    name = models.TextField(max_length=SHORT_TEXT_MAX)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name='products')
    supplier = models.ForeignKey('Supplier', on_delete=models.CASCADE, related_name='products')
    price = PositiveDecimalField(
        decimal_places=2, max_digits=10, validators=[check_positive],
    )

    def __str__(self) -> str:
        """
        Return self name.

        Returns:
            str (str): name and price
        """
        return f'{self.name} - {self.price}'

    class Meta:
        """Meta."""

        ordering = ['category']


def check_rating(rating: int) -> None:
    """
    Validate to ensure a rating is between 0 and 5.

    Args:
        rating (int): The rating to check.

    Raises:
        ValidationError: If the rating is not between 0 and 5.
    """
    if 0 <= rating <= 5:
        return
    raise ValidationError(
        'rating should be between 0 and 5',
    )


class Review(UUIDMixin, OwnerMixin):
    """
    Model representing a product review.

    Fields:
        product_id: The ID of the product being reviewed.
        text: The text content of the review.
        rating: The rating given in the review.
    """

    product_id = models.ForeignKey(Product, models.CASCADE, related_name='reviews')
    text = models.TextField(blank=True, null=True, max_length=LONG_TEXT_MAX)
    rating = models.PositiveIntegerField(validators=[check_rating])

    def __str__(self) -> str:
        """
        Return self rating and name.

        Returns:
            str: rating and name
        """
        return '{0} - {1}'.format(self.rating, self.product_id.name)

    class Meta:
        """Meta."""

        ordering = ['rating']


PHONE_REGEX = r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$'


def check_phone(phone: str) -> None:
    """
    Validate to ensure a phone number matches a specific pattern.

    Args:
        phone (str): The phone number to check.

    Raises:
        ValidationError: If the phone number is not valid.
    """
    if not re.match(PHONE_REGEX, phone):
        raise ValidationError(
            'invalid phone number: %(phone)s',
            params={'phone': phone},
        )


class Supplier(UUIDMixin):
    """
    Model representing a supplier.

    Fields:
        owner: The user who owns the supplier.
        name: The name of the supplier.
        phone: The phone number of the supplier.
    """

    owner = models.OneToOneField(
        'auth.User', related_name='%(class)s', on_delete=models.CASCADE,
    )
    name = models.TextField(max_length=SHORT_TEXT_MAX)
    phone = models.TextField(
        max_length=SHORT_TEXT_MAX,
        validators=[check_phone],
    )

    def __str__(self) -> str:
        """
        Return self name.

        Returns:
            name (str): name
        """
        return f'{self.name}'

    class Meta:
        """Meta."""

        ordering = ['name']

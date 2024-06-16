from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.db import models
from django import forms
from uuid import uuid4
import re


class UUIDMixin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True


class OwnerMixin(models.Model):
    owner = models.ForeignKey(
        "auth.User", related_name="%(class)s", on_delete=models.CASCADE)

    class Meta:
        abstract = True


class PositiveDecimalField(models.DecimalField):
    def formfield(self, **kwargs):
        return super().formfield(
            **{
                "min_value": 0,
                "max_digits": self.max_digits,
                "decimal_places": self.decimal_places,
                "form_class": forms.DecimalField,
                **kwargs,
            }
        )


SHORT_TEXT_MAX = 100
LONG_TEXT_MAX = 1000


class Category(UUIDMixin):
    name = models.TextField(max_length=SHORT_TEXT_MAX)
    description = models.TextField(max_length=LONG_TEXT_MAX, blank=True)
    products = models.ManyToManyField("Product", through="ProductCategory")

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name_plural = _("categories")
        ordering = ["name"]


def check_positive(num: int) -> None:
    if num < 0:
        raise ValidationError("price should be bigger than zero")


class Product(UUIDMixin, OwnerMixin):
    name = models.TextField(max_length=SHORT_TEXT_MAX)
    category_id = models.ManyToManyField(Category)
    suppliers = models.ManyToManyField("Supplier", through="ProductSupplier")
    price = PositiveDecimalField(
        decimal_places=2, max_digits=10, validators=[check_positive]
    )

    def __str__(self) -> str:
        return f"{self.name} - {self.price}"

    class Meta:
        ordering = ["category"]


def check_rating(rating: int) -> None:
    if 0 <= rating <= 5:
        return
    raise ValidationError(
        "rating should be between 0 and 5",
    )


class Review(UUIDMixin, OwnerMixin):
    product_id = models.ForeignKey(Product, models.CASCADE)
    text = models.TextField(blank=True, null=True, max_length=LONG_TEXT_MAX)
    rating = models.PositiveIntegerField(validators=[check_rating])

    def __str__(self) -> str:
        return f"{self.rating} - {self.product_id.name}"

    class Meta:
        ordering = ["rating"]


PHONE_REGEX = r"^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$"


def check_phone(phone: str) -> None:
    if not re.match(PHONE_REGEX, phone):
        raise ValidationError(
            "invalid phone number: %(phone)s",
            params={"phone": phone},
        )


class Supplier(UUIDMixin, OwnerMixin):
    name = models.TextField(max_length=SHORT_TEXT_MAX)
    phone = models.TextField(max_length=SHORT_TEXT_MAX,
                             validators=[check_phone])
    products = models.ManyToManyField("Product", through="ProductSupplier")

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        ordering = ["name"]


class ProductSupplier(models.Model):
    product_id = models.ForeignKey(Product, models.DO_NOTHING)
    supplier_id = models.ForeignKey(Supplier, models.DO_NOTHING)

    def __str__(self) -> str:
        return f"{self.product_id.name} - {self.supplier_id.name}"

    class Meta:
        unique_together = ("product_id", "supplier_id")

        verbose_name = _("relationship product supplier")
        verbose_name_plural = _("relationships product supplier")


class ProductCategory(models.Model):
    product_id = models.OneToOneField(Product, models.DO_NOTHING)
    category_id = models.ForeignKey(Category, models.DO_NOTHING)

    def __str__(self) -> str:
        return f"{self.product_id.name} - {self.product_id.name}"

    class Meta:
        verbose_name = _("relationship product supplier")
        verbose_name_plural = _("relationships product supplier")

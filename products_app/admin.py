"""Admin panel."""

from django.contrib import admin

from .models import Category, Product, Review, Supplier


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Product admin panel."""

    model = Product


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    """Supplier admin panel."""

    model = Supplier


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Review admin panel."""

    model = Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category admin panel."""

    model = Category

from django.contrib import admin
from .models import (
    Product,
    Review,
    Supplier,
    ProductSupplier,
    Category,
    ProductCategory,
)


class ProductSupplierInline(admin.TabularInline):
    model = ProductSupplier
    extra = 1


class CategoryProductInline(admin.TabularInline):
    model = ProductCategory
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product
    inlines = [ProductSupplierInline, CategoryProductInline]


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    model = Supplier
    inlines = [ProductSupplierInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    model = Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    inlines = [CategoryProductInline]

from django import forms
from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import (
    Category,
    Product,
    ProductImage,
    ProductSpecs,
    ProductSpecsValue,
    ProductType,
)

admin.site.register(Category, MPTTModelAdmin)


# TabularInline allow inputting data into 2 related tables at the same time
class ProductSpecsInline(admin.TabularInline):
    model = ProductSpecs


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [
        ProductSpecsInline,
    ]


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class ProductSpecsValueInline(admin.TabularInline):
    model = ProductSpecsValue


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductSpecsValueInline,
        ProductImageInline,
    ]

from django.contrib import admin
from .models import Category, Brand, Product, ProductImage, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ["id", "name", "slug"]

    prepopulated_fields = {
        "slug": ("name",)
    }


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):

    list_display = ["id", "name"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "name",
        "category",
        "brand",
        "price",
        "stock",
        "available",
        "created_at",
    ]

    list_filter = [
        "category",
        "brand",
        "available",
    ]

    search_fields = [
        "name",
        "description",
    ]

    ordering = [
        "-created_at",
    ]

    prepopulated_fields = {
        "slug": ("name",)
    }


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "product",
        "image",
    ]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "product",
        "user",
        "rating",
        "created_at",
    ]

    list_filter = [
        "rating",
    ]
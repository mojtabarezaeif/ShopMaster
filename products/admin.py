from django.contrib import admin
from .models import Category, Brand, Product, ProductImage, Review
from .models import Wishlist, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ["id", "name", "slug"]

    prepopulated_fields = {
        "slug": ("name",)
    }


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):

    list_display = ["id", "name"]

from django.utils.html import format_html

class ProductImageInline(admin.TabularInline):

    model = ProductImage

    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "image_preview",
        "name",
        "category",
        "brand",
        "price",
        "stock",
        "available",
    ]

    def image_preview(self, obj):

        image = obj.images.first()

        if image:

            return format_html(

                '<img src="{}" width="70">',

                image.image.url

            )

        return "-"

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

    inlines = [
        ProductImageInline,
    ]

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):

    list_display = [
        "id",
        "product",
        "image",
    ]

    def thumbnail(self, obj):

        if obj.image:

            return format_html(
                '<img src="{}" width="70">',
                obj.image.url
            )

        return "-"
    
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

    search_fields = [
        "comment",
    ]

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "product",
        "created_at",
    )
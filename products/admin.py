from django.contrib import admin

# Register your models here.
from .models import (
    Category,
    Brand,
    Product,
    ProductImage,
    Review,
)

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Review)
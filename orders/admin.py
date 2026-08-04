from django.contrib import admin

# Register your models here.
from .models import Order, OrderItem
from .models import Coupon

class OrderItemInline(admin.TabularInline):

    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (

        "id",
        "full_name",
        "status",
        "created_at",
    )

    list_filter = (

        "status",
        "created_at",
    )

    search_fields = (

        "full_name",
        "email",
    )

    inlines = [

        OrderItemInline

    ]

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):

    list_display = (

        "code",

        "discount",

        "active",

        "valid_from",

        "valid_to",

    )

    list_filter = (

        "active",

    )
from django.contrib import admin
from .models import Order, OrderItem, Coupon


class OrderItemInline(admin.TabularInline):

    model = OrderItem

    extra = 0

    readonly_fields = (
        "product",
        "price",
        "quantity",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "full_name",
        "email",
        "status",
        "final_price",
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

    readonly_fields = (
        "created_at",
        "paid_at",
        "transaction_id",
    )

    inlines = [
        OrderItemInline,
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

    search_fields = (
        "code",
    )
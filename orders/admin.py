from django.contrib import admin

# Register your models here.
from .models import Order, OrderItem

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
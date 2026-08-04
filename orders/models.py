from django.db import models

# Create your models here.
from products.models import Product
from django.contrib.auth.models import User

class Order(models.Model):

    full_name = models.CharField(
        max_length=100
    )

    email = models.EmailField()

    address = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    STATUS_CHOICES = [

        ("pending", "Pending"),
        ("paid", "Paid"),
        ("processing", "Processing"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
    )

    def __str__(self):

        return f"Order {self.id}"

    @property
    def total_price(self):

        return sum(

            item.total_price

            for item in self.items.all()

        )

    class Meta:
        ordering = ["-created_at"]


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE
    )


    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )


    price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )


    quantity = models.PositiveIntegerField()


    def get_total_price(self):

        return self.price * self.quantity

    @property
    def total_price(self):

        return self.price * self.quantity

from django.utils import timezone

class Coupon(models.Model):

    code = models.CharField(
        max_length=30,
        unique=True
    )

    discount = models.PositiveIntegerField()

    active = models.BooleanField(
        default=True
    )

    valid_from = models.DateTimeField()

    valid_to = models.DateTimeField()

    def __str__(self):

        return self.code
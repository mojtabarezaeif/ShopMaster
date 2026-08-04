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

    def __str__(self):

        return f"Order {self.id}"



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
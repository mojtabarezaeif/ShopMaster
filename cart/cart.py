from decimal import Decimal

from products.models import Product


class Cart:

    def __init__(self, request):

        self.session = request.session

        cart = self.session.get("cart")

        if not cart:

            cart = self.session["cart"] = {}

        self.cart = cart

    def add(self, product, quantity=1):

        product_id = str(product.id)

        if product_id not in self.cart:

            self.cart[product_id] = {

                "quantity": quantity

            }

        else:

            self.cart[product_id]["quantity"] += quantity

        self.save()

    def save(self):

        self.session.modified = True

    def remove(self, product):

        product_id = str(product.id)

        if product_id in self.cart:

            del self.cart[product_id]

            self.save()

    def clear(self):

        self.session["cart"] = {}

        self.save()

    def __len__(self):

        return sum(

            item["quantity"]

            for item in self.cart.values()

        )
from decimal import Decimal

from orders.models import Coupon
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

        current_quantity = self.cart.get(

            product_id,

            {}

        ).get(

            "quantity",

            0

        )

        new_quantity = current_quantity + quantity

        if new_quantity > product.stock:

            new_quantity = product.stock

        self.cart[product_id] = {

            "quantity": new_quantity

        }

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

    def __iter__(self):

        product_ids = self.cart.keys()

        products = Product.objects.filter(

            id__in=product_ids

        )

        cart = self.cart.copy()

        for product in products:

            cart[str(product.id)]["product"] = product

        for item in cart.values():

            item["total_price"] = (

                item["product"].price

                *

                item["quantity"]

            )

            yield item

    def get_total_price(self):

        total = Decimal("0")

        for item in self:

            total += item["total_price"]

        return total

    def update(self, product, quantity):

        product_id = str(product.id)

        if product_id in self.cart:

            self.cart[product_id]["quantity"] = quantity

            if quantity <= 0:

                del self.cart[product_id]

            self.save()

    def get_discount(self, coupon):

        if not coupon:

            return Decimal("0")

        return (

            self.get_total_price()

            *

            Decimal(coupon.discount)

            /

            Decimal("100")

        )

    def get_final_price(self, coupon):

        return (

            self.get_total_price()

            -

            self.get_discount(coupon)

        )
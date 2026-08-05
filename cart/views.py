from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect, get_object_or_404
from products.models import Product
from .cart import Cart
from django.contrib import messages

def cart_add(request, product_id):

    cart = Cart(request)

    product = get_object_or_404(
        Product,
        id=product_id
    )

    cart.add(product)

    messages.success(

        request,

        "Product added to cart."

    )

    return redirect("cart_detail")


def cart_detail(request):

    cart = Cart(request)

    return render(

        request,

        "cart/cart_detail.html",

        {

            "cart": cart

        }

    )

def cart_remove(request, product_id):

    cart = Cart(request)

    product = get_object_or_404(
        Product,
        id=product_id
    )

    cart.remove(product)

    messages.success(
        request,
        "Product removed from cart."
    )

    return redirect("cart_detail")

def cart_update(request, product_id):

    cart = Cart(request)

    product = get_object_or_404(
        Product,
        id=product_id
    )

    quantity = int(request.POST.get("quantity"))

    # اگر بیشتر از موجودی خواسته شد
    if quantity > product.stock:

        quantity = product.stock

        messages.warning(
            request,
            f"Only {product.stock} item(s) available."
        )

    cart.update(product, quantity)

    return redirect("cart_detail")
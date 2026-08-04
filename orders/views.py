from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
from .forms import OrderForm
from .models import Order, OrderItem
from cart.cart import Cart
from django.contrib.auth.decorators import login_required

def checkout(request):

    cart = Cart(request)


    if request.method == "POST":


        form = OrderForm(request.POST)


        if form.is_valid():


            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                full_name=form.cleaned_data["full_name"],
                email=form.cleaned_data["email"],
                address=form.cleaned_data["address"],
            )


            for item in cart:


                OrderItem.objects.create(

                    order=order,

                    product=item["product"],

                    price=item["product"].price,

                    quantity=item["quantity"]

                )


            cart.clear()


            return redirect("cart_detail")


    else:

        form = OrderForm()


    return render(

        request,

        "orders/checkout.html",

        {

            "form": form,

            "cart": cart

        }

    )


@login_required
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "orders/my_orders.html",
        {
            "orders": orders
        }
    )
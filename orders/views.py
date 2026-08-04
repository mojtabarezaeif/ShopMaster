from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .forms import OrderForm
from .models import Order, OrderItem
from cart.cart import Cart

def checkout(request):

    cart = Cart(request)


    if request.method == "POST":


        form = OrderForm(request.POST)


        if form.is_valid():


            order = Order.objects.create(

                full_name=form.cleaned_data["full_name"],

                email=form.cleaned_data["email"],

                address=form.cleaned_data["address"]

            )


            for item in cart:


                OrderItem.objects.create(

                    order=order,

                    product=item["product"],

                    price=item["product"].price,

                    quantity=item["quantity"]

                )


            cart.clear()


            return redirect(
                "order_success"
            )


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
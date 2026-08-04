from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
from .forms import OrderForm
from .models import Order, OrderItem
from cart.cart import Cart
from django.contrib.auth.decorators import login_required
from .models import Coupon
from .forms import CouponApplyForm
from django.utils import timezone
from django.contrib import messages


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

            request.session["order_id"] = order.id

            for item in cart:


                OrderItem.objects.create(

                    order=order,

                    product=item["product"],

                    price=item["product"].price,

                    quantity=item["quantity"]

                )


            cart.clear()


            return redirect("payment_page")


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


def apply_coupon(request):

    if request.method == "POST":

        form = CouponApplyForm(request.POST)

        if form.is_valid():

            code = form.cleaned_data["code"]

            coupon = Coupon.objects.filter(

                code__iexact=code,

                active=True,

                valid_from__lte=timezone.now(),

                valid_to__gte=timezone.now()

            ).first()

            if coupon:

                request.session["coupon_id"] = coupon.id

                messages.success(

                    request,

                    "Coupon applied."

                )

            else:

                request.session["coupon_id"] = None

                messages.error(

                    request,

                    "Invalid coupon."

                )

    return redirect("cart_detail")
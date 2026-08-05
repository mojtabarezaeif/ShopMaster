from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages

from .forms import OrderForm
from .models import Order, OrderItem, Coupon
from cart.cart import Cart


def checkout(request):

    cart = Cart(request)

    coupon = None

    coupon_id = request.session.get("coupon_id")

    if coupon_id:

        try:

            coupon = Coupon.objects.get(id=coupon_id)

        except Coupon.DoesNotExist:

            request.session["coupon_id"] = None

    # ----------------------------
    # محاسبه قیمت‌ها
    # ----------------------------

    subtotal = cart.get_total_price()

    discount = 0

    final_price = subtotal

    if coupon:

        discount = cart.get_discount(coupon)

        final_price = cart.get_final_price(coupon)

    # ----------------------------

    if request.method == "POST":

        form = OrderForm(request.POST)

        if form.is_valid():

            order = Order.objects.create(

                user=request.user if request.user.is_authenticated else None,

                full_name=form.cleaned_data["full_name"],

                email=form.cleaned_data["email"],

                address=form.cleaned_data["address"],

                coupon=coupon,

                subtotal=subtotal,

                discount_amount=discount,

                final_price=final_price,

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

            request.session.pop("coupon_id", None)

            return redirect("payment_page")

    else:

        form = OrderForm()

    return render(

        request,

        "orders/checkout.html",

        {

            "form": form,

            "cart": cart,

            "coupon": coupon,

            "discount": discount,

            "subtotal": subtotal,

            "final_price": final_price,

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

        code = request.POST.get("code")

        try:

            coupon = Coupon.objects.get(

                code=code,

                active=True,

                valid_from__lte=timezone.now(),

                valid_to__gte=timezone.now()

            )

            request.session["coupon_id"] = coupon.id

            messages.success(

                request,

                "Coupon applied successfully."

            )

        except Coupon.DoesNotExist:

            request.session["coupon_id"] = None

            messages.error(

                request,

                "Invalid or expired coupon."

            )

    return redirect("checkout")
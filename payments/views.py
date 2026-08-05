from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import uuid
from orders.models import Order

@login_required
def payment_page(request):

    return render(
        request,
        "payments/payment_page.html"
    )


@login_required
def payment_success(request):

    order_id = request.session.get("order_id")

    if order_id:

        order = Order.objects.get(id=order_id)

        order.status = "paid"

        for item in order.items.all():

            product = item.product

            product.stock -= item.quantity

            if product.stock < 0:

                product.stock = 0

            product.save()

        order.transaction_id = str(uuid.uuid4())

        order.paid_at = timezone.now()

        order.save()

    return render(

        request,

        "payments/payment_success.html"

    )


@login_required
def payment_failed(request):

    return render(
        request,
        "payments/payment_failed.html"
    )
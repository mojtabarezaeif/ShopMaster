from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from orders.models import Order
from products.models import Wishlist
from .forms import ProfileForm

def register(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():

            form.save()

            messages.success(

                request,

                "Registration completed successfully."

            )

            return redirect("login")

    else:

        form = RegisterForm()

    return render(

        request,

        "accounts/register.html",

        {

            "form": form

        }

    )


@login_required
def dashboard(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by("-created_at")

    wishlist_count = Wishlist.objects.filter(

        user=request.user

    ).count()

    context = {

        "orders": orders,

        "wishlist_count": wishlist_count,

    }

    return render(

        request,

        "accounts/dashboard.html",

        context

    )

@login_required
def edit_profile(request):

    if request.method == "POST":

        form = ProfileForm(

            request.POST,

            instance=request.user

        )

        if form.is_valid():

            form.save()

            messages.success(

                request,

                "Profile updated successfully."

            )

            return redirect("dashboard")

    else:

        form = ProfileForm(

            instance=request.user

        )

    return render(

        request,

        "accounts/edit_profile.html",

        {

            "form": form

        }

    )
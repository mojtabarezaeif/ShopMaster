from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
from .forms import RegisterForm
from django.contrib import messages


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
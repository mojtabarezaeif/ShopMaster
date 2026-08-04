from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView
from .models import Product


class ProductListView(ListView):

    model = Product

    template_name = "products/product_list.html"

    context_object_name = "products"

    paginate_by = 8

    queryset = Product.objects.filter(
        available=True
    )


class ProductDetailView(DetailView):

    model = Product

    template_name = "products/product_detail.html"

    context_object_name = "product"

    slug_field = "slug"

    slug_url_kwarg = "slug"
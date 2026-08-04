from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView
from .models import Product


from django.views.generic import ListView
from django.db.models import Q

from .models import Product, Category, Brand


class ProductListView(ListView):

    model = Product

    template_name = "products/product_list.html"

    context_object_name = "products"

    paginate_by = 8

    def get_queryset(self):

        queryset = Product.objects.filter(
            available=True
        )

        search = self.request.GET.get("q")

        if search:

            queryset = queryset.filter(

                Q(name__icontains=search)

                |

                Q(description__icontains=search)

                |

                Q(category__name__icontains=search)

                |

                Q(brand__name__icontains=search)

            )

        category = self.request.GET.get("category")

        if category:

            queryset = queryset.filter(
                category__slug=category
            )

        brand = self.request.GET.get("brand")

        if brand:

            queryset = queryset.filter(
                brand__id=brand
            )

        sort = self.request.GET.get("sort")

        if sort == "newest":

            queryset = queryset.order_by("-created_at")

        elif sort == "price_low":

            queryset = queryset.order_by("price")

        elif sort == "price_high":

            queryset = queryset.order_by("-price")

        elif sort == "name":

            queryset = queryset.order_by("name")

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["categories"] = Category.objects.all()

        context["brands"] = Brand.objects.all()

        return context


class ProductDetailView(DetailView):

    model = Product

    template_name = "products/product_detail.html"

    context_object_name = "product"

    slug_field = "slug"

    slug_url_kwarg = "slug"
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView
from .models import Product
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from .models import Wishlist
from django.views.generic import ListView
from django.db.models import Q
from .models import Product, Category, Brand
from django.contrib import messages
from .forms import ReviewForm
from .models import Review
from django.db.models import Avg

from django.contrib.auth.decorators import login_required

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

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["form"] = ReviewForm()

        context["reviews"] = self.object.reviews.all()

        context["average_rating"] = (
            self.object.reviews.aggregate(
                Avg("rating")
            )["rating__avg"]
        )

        context["related_products"] = Product.objects.filter(
            category=self.object.category,
            available=True
        ).exclude(
            id=self.object.id
        )[:4]

        return context

@login_required
def add_to_wishlist(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    Wishlist.objects.get_or_create(

        user=request.user,

        product=product

    )

    messages.success(

        request,

        "Added to wishlist."

    )

    return redirect(
        "product_detail",
        slug=product.slug
    )


@login_required
def wishlist(request):

    wishlist = Wishlist.objects.filter(

        user=request.user

    ).select_related("product")

    return render(

        request,

        "products/wishlist.html",

        {

            "wishlist": wishlist

        }

    )


@login_required
def remove_from_wishlist(request, product_id):

    Wishlist.objects.filter(

        user=request.user,

        product_id=product_id

    ).delete()

    messages.success(

        request,

        "Removed from wishlist."

    )

    return redirect("wishlist")


@login_required
def add_review(request, slug):

    product = get_object_or_404(

        Product,

        slug=slug

    )

    if request.method == "POST":

        form = ReviewForm(request.POST)

        if form.is_valid():

            Review.objects.update_or_create(

                product=product,

                user=request.user,

                defaults={

                    "rating": form.cleaned_data["rating"],

                    "comment": form.cleaned_data["comment"]

                }

            )

            messages.success(

                request,

                "Review saved."

            )

    return redirect(

        "product_detail",

        slug=slug

    )
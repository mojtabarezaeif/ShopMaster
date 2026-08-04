from django.urls import path
from .views import ProductListView, ProductDetailView
from . import views

urlpatterns = [

    path(
        "",
        ProductListView.as_view(),
        name="product_list"
    ),

    path(
        "wishlist/<int:product_id>/",
        views.add_to_wishlist,
        name="add_to_wishlist"
    ),

    path(
    "wishlist/",
    views.wishlist,
    name="wishlist",
    ),

    path(
        "wishlist/remove/<int:product_id>/",
        views.remove_from_wishlist,
        name="remove_from_wishlist",
    ),

    path(
        "<slug:slug>/",
        ProductDetailView.as_view(),
        name="product_detail"
    ),
]
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("cars/", views.cars, name="cars"),
    path("cars/<int:car_id>", views.car, name="car"),
    path("orders/", views.OrdersListView.as_view(), name="orders_link"),
    path("orders/<int:pk>", views.OrdersDetailView.as_view(), name="orders_detail"),
    path("search/", views.search, name="search_link"),
    path("accounts/", include("django.contrib.auth.urls"))
]

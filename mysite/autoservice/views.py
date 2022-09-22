from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import AutomobilioModelis, Automobilis, Uzsakymas, UzsakymoEilute, Paslauga


def index(request):
    num_paslaugos = Paslauga.objects.count()
    num_ivykdyti = Uzsakymas.objects.filter(status="i").count()
    num_automobiliai = Automobilis.objects.count()
    kontext = {
        "num_paslaugos": num_paslaugos,
        "num_ivykdyti": num_ivykdyti,
        "num_automobiliai": num_automobiliai,
    }
    return render(request, "index.html", context=kontext)


def cars(request):
    automobiliai = Automobilis.objects.all()
    kontext = {"automobiliai": automobiliai}
    return render(request, "cars.html", context=kontext)


def car(request, car_id):
    car_info = get_object_or_404(Automobilis, pk=car_id)
    paslauga_info = Uzsakymas.objects.filter(automobilis_id=car_id)
    kontext = {"car_info": car_info,
               "paslauga": paslauga_info}
    return render(request, "car.html", context=kontext)


class OrdersListView(generic.ListView):
    model = Uzsakymas
    template_name = "order_list.html"


class OrdersDetailView(generic.DetailView):
    model = Uzsakymas
    template_name = "order_detail.html"

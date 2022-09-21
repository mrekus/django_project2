from django.shortcuts import render
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

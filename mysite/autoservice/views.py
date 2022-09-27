from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import AutomobilioModelis, Automobilis, Uzsakymas, UzsakymoEilute, Paslauga


def index(request):
    num_paslaugos = Paslauga.objects.count()
    num_ivykdyti = Uzsakymas.objects.filter(status="i").count()
    num_automobiliai = Automobilis.objects.count()
    num_visits = request.session.get("num_visits", 1)
    request.session["num_visits"] = num_visits + 1
    kontext = {
        "num_paslaugos": num_paslaugos,
        "num_ivykdyti": num_ivykdyti,
        "num_automobiliai": num_automobiliai,
        "num_visits": num_visits
    }
    return render(request, "index.html", context=kontext)


def cars(request):
    paginator = Paginator(Automobilis.objects.all(), 1)
    page_number = request.GET.get("page")
    paged_cars = paginator.get_page(page_number)
    kontext = {"automobiliai": paged_cars}
    return render(request, "cars.html", context=kontext)


def car(request, car_id):
    car_info = get_object_or_404(Automobilis, pk=car_id)
    paslauga_info = Uzsakymas.objects.filter(automobilis_id=car_id)
    kontext = {"car_info": car_info, "paslauga": paslauga_info}
    return render(request, "car.html", context=kontext)


def search(request):
    query_text = request.GET.get("query")
    search_results = Automobilis.objects.filter(
        Q(valstybinis_nr__icontains=query_text)
        | Q(VIN_kodas__icontains=query_text)
        | Q(klientas__icontains=query_text)
        | Q(automobilio_modelis_id__modelis__icontains=query_text)
        | Q(automobilio_modelis_id__marke__icontains=query_text)
    )
    return render(
        request, "search.html", {"cars": search_results, "querytxt": query_text}
    )


class OrdersListView(generic.ListView):
    model = Uzsakymas
    paginate_by = 2
    template_name = "order_list.html"


class OrdersDetailView(generic.DetailView):
    model = Uzsakymas
    template_name = "order_detail.html"


class OrdersByUserListView(LoginRequiredMixin, generic.ListView):
    model = Uzsakymas  # konteksto kint į šabloną bookinstance_list
    template_name = "user_orders.html"
    paginate_by = 10

    def get_queryset(self):
        return (
            Uzsakymas.objects.filter(vartotojas=self.request.user)
            .order_by("grazinimas")
        )

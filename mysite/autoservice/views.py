from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import AutomobilioModelis, Automobilis, Uzsakymas, UzsakymoEilute, Paslauga
from .forms import UzsakymoReviewForm, ProfilisUpdateForm, UserUpdateForm
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.views.generic.edit import FormMixin
import re


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
        "num_visits": num_visits,
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


class OrdersDetailView(generic.DetailView, FormMixin):
    model = Uzsakymas
    template_name = "order_detail.html"
    form_class = UzsakymoReviewForm

    class Meta:
        ordering = ["data"]

    def get_success_url(self):
        return reverse("orders_detail", kwargs={"pk": self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.uzsakymas = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super(OrdersDetailView, self).form_valid(form)


class OrdersByUserListView(LoginRequiredMixin, generic.ListView):
    model = Uzsakymas  # konteksto kint į šabloną bookinstance_list
    template_name = "user_orders.html"
    paginate_by = 10

    def get_queryset(self):
        return Uzsakymas.objects.filter(vartotojas=self.request.user).order_by(
            "grazinimas"
        )


@csrf_protect
def register(request):
    if request.method == "POST":
        laukai = [
            request.POST["username"],
            request.POST["email"],
            request.POST["password"],
            request.POST["password2"],
        ]
        username, email, password, password2 = laukai
        if all(laukai):
            if password == password2:
                if re.match(r"[A-Za-z\d]{8,}", password):
                    if User.objects.filter(username=username).exists():
                        messages.error(request, f"Vartotojo vardas {username} užimtas!")
                        return redirect("register")
                    else:
                        if User.objects.filter(email=email).exists():
                            messages.error(
                                request,
                                f"Vartotojas su el. paštu {email} jau užregistruotas!",
                            )
                            return redirect("register")
                        else:
                            User.objects.create_user(
                                username=username, email=email, password=password
                            )
                            messages.success(request, f"Vartotojas {username} sukurtas!")
                else:
                    messages.error(request, f"Slaptažodis per silpnas!")
                    return redirect("register")
            else:
                messages.error(request, f"Slaptažodžiai nesutampa!")
                return redirect("register")
        else:
            messages.error(request, f"Yra neužpildytų laukų!")
            return redirect("register")
    return render(request, "register.html")


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfilisUpdateForm(request.POST, request.FILES, instance=request.user.profilis)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Profilis atnaujintas")
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfilisUpdateForm(instance=request.user.profilis)
    context = {
        "u_form": u_form,
        "p_form": p_form
    }
    return render(request, "profile.html", context=context)

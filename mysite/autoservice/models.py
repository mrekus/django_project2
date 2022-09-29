from django.db import models
from django.contrib.auth.models import User
from datetime import date
from tinymce.models import HTMLField


class AutomobilioModelis(models.Model):
    marke = models.CharField(
        "Markė", max_length=50, help_text="Įveskite automobilio markę"
    )
    modelis = models.CharField(
        "Modelis", max_length=50, help_text="Įveskite automobilio modelį"
    )

    class Meta:
        verbose_name = "Automobilio modelis"
        verbose_name_plural = "Automobilių modeliai"

    def __str__(self):
        return f"{self.marke} {self.modelis}"


class Automobilis(models.Model):
    valstybinis_nr = models.CharField("Valstybinis_NR", max_length=7)
    automobilio_modelis_id = models.ForeignKey(
        "AutomobilioModelis", on_delete=models.SET_NULL, null=True
    )
    VIN_kodas = models.CharField(
        "VIN_kodas", max_length=200, help_text="Įveskite VIN kodą"
    )
    klientas = models.CharField("Klientas", max_length=200)
    nuotrauka = models.ImageField("Nuotrauka", upload_to="auto_nuotraukos", null=True)
    aprasymas = HTMLField()

    class Meta:
        verbose_name = "Automobilis"
        verbose_name_plural = "Automobiliai"

    def __str__(self):
        return f"{self.automobilio_modelis_id} {self.VIN_kodas}"


class Uzsakymas(models.Model):
    data = models.DateField("Data", null=True, blank=True)
    automobilis_id = models.ForeignKey(
        "Automobilis", on_delete=models.SET_NULL, null=True
    )
    grazinimas = models.DateField("Bus įvykdyta", null=True, blank=True)

    UZSAKYMO_STATUS = (
        ("p", "Priimtas"),
        ("v", "Vykdomas"),
        ("i", "Įvykdytas"),
        ("a", "Atmestas"),
    )

    status = models.CharField(
        max_length=1,
        choices=UZSAKYMO_STATUS,
        blank=True,
        default="p", 
        help_text="Statusas",
    )

    vartotojas = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        if self.grazinimas and date.today() > self.grazinimas:
            return True
        return False

    @property
    def suma(self):
        kainos = UzsakymoEilute.objects.filter(uzsakymas_id=self.id).all()
        suma = 0
        for i in kainos:
            suma += i.kaina
        return suma

    class Meta:
        verbose_name = "Užsakymas"
        verbose_name_plural = "Užsakymai"

    def __str__(self):
        return f"{self.data} {self.automobilis_id}"


class UzsakymoReview(models.Model):
    uzsakymas = models.ForeignKey("Uzsakymas", on_delete=models.SET_NULL, null=True)
    reviewer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField("Atsiliepimas", max_length=2000)


class UzsakymoEilute(models.Model):
    paslauga_id = models.ForeignKey("Paslauga", on_delete=models.SET_NULL, null=True)
    uzsakymas_id = models.ForeignKey(
        "Uzsakymas", on_delete=models.SET_NULL, null=True, related_name="uzsakymoeilute"
    )
    kiekis = models.IntegerField("Kiekis")

    @property
    def kaina(self):
        kaina = self.paslauga_id.kaina * self.kiekis
        return kaina

    class Meta:
        verbose_name = "Užsakymo eilutė"
        verbose_name_plural = "Užsakymų eilutės"

    def __str__(self):
        return f"{self.uzsakymas_id} - {self.paslauga_id} - {self.kiekis}"


class Paslauga(models.Model):
    pavadinimas = models.CharField("Pavadinimas", max_length=200)
    kaina = models.FloatField("Kaina")

    class Meta:
        verbose_name = "Paslauga"
        verbose_name_plural = "Paslaugos"

    def __str__(self):
        return self.pavadinimas


class Profilis(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nuotrauka = models.ImageField(default="blank.png", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} profilis"

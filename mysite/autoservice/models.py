from django.db import models


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
    suma = models.FloatField("Suma", max_length=200)

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

    class Meta:
        verbose_name = "Užsakymas"
        verbose_name_plural = "Užsakymai"

    def __str__(self):
        return f"{self.data} {self.automobilis_id}"


class UzsakymoEilute(models.Model):
    paslauga_id = models.ForeignKey("Paslauga", on_delete=models.SET_NULL, null=True)
    uzsakymas_id = models.ForeignKey(
        "Uzsakymas", on_delete=models.SET_NULL, null=True, related_name="uzsakymoeilute"
    )
    kiekis = models.IntegerField("Kiekis")
    kaina = models.FloatField("Kaina", max_length=200)

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

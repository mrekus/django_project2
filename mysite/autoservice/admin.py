from django.contrib import admin
from .models import AutomobilioModelis, Automobilis, Uzsakymas, UzsakymoEilute, Paslauga, UzsakymoReview
from django import forms


# class UzsakymasInlineForm(forms.ModelForm):
#     kaina = forms.ModelChoiceField(queryset=Paslauga.objects.values_list('kaina', flat=True))


class UzsakymasInline(admin.TabularInline):
    model = UzsakymoEilute
    # form = UzsakymasInlineForm
    # readonly_fields = ("kaina",)
    can_delete = False
    extra = 0


class UzsakymasAdmin(admin.ModelAdmin):
    inlines = [UzsakymasInline]
    list_display = ("automobilis_id", "data", "vartotojas", "grazinimas", "suma")


class AutomobilisAdmin(admin.ModelAdmin):
    list_display = ("klientas", "automobilio_modelis_id", "valstybinis_nr", "VIN_kodas", "aprasymas")
    list_filter = ("klientas", "automobilio_modelis_id")
    search_fields = ("valstybinis_nr", "VIN_kodas")


class PaslaugaAdmin(admin.ModelAdmin):
    list_display = ("pavadinimas", "kaina")


class UzsakymoReviewAdmin(admin.ModelAdmin):
    list_display = ("uzsakymas", "date_created", "reviewer", "content")


admin.site.register(AutomobilioModelis)
admin.site.register(Automobilis, AutomobilisAdmin)
admin.site.register(Uzsakymas, UzsakymasAdmin)
admin.site.register(UzsakymoEilute)
admin.site.register(Paslauga, PaslaugaAdmin)
admin.site.register(UzsakymoReview, UzsakymoReviewAdmin)

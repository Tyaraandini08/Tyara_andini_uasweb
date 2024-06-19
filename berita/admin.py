from django.contrib import admin
from berita.models import Kategori, Artikel

admin.site.register(Kategori)

# Register your models here.
class ArtikelAdmin(admin.ModelAdmin):
    list_display = ["judul","kategori","author"]
    search_fields = ["judul"]
admin.site.register(Artikel, ArtikelAdmin)
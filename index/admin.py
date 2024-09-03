from django.contrib import admin
from index.models import Faq, About, Personnel, Footer

admin.site.register(Faq)

class PersonnelAdmin(admin.TabularInline):
    model = Personnel

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    inlines = (PersonnelAdmin,)

admin.site.register(Footer)
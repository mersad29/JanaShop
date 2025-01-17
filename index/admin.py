from django.contrib import admin
from index.models import Faq, About, Personnel, Footer
from product.models import Category, FeaturedCategory

admin.site.register(Faq)

class PersonnelAdmin(admin.TabularInline):
    model = Personnel

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    inlines = (PersonnelAdmin,)

admin.site.register(Footer)

@admin.register(FeaturedCategory)
class FeaturedCategoryAdmin(admin.ModelAdmin):
    list_display = ['category', 'is_active']
    list_filter = ['is_active']
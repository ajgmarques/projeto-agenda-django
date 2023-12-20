from django.contrib import admin
from contact.models import Contact, Category

# Register your models here.


@admin.register(Contact)
class ContacAdmin(admin.ModelAdmin):
    list_display = 'id', 'first_name', 'last_name', 'phone', 'email', 'show',
    ordering = '-id',
    list_filter = 'created_date',
    search_fields = 'id', 'first_name', 'last_name', 'email',
    list_per_page = 20
    list_max_show_all = 200
    list_editable = 'phone', 'email', 'show',
    list_display_links = 'id', 'first_name'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'name',
    ordering = 'name',

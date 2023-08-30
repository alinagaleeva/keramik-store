from django.contrib import admin

from .models import Bag, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity')
    fields = ('name', 'description', ('price', 'quantity'), ('image_main', 'image_addition'))
    search_fields = ('name',)
    ordering = ('name',)


class BagAdmin(admin.TabularInline):
    model = Bag
    fields = ('product', 'quantity', 'created_timestamp')
    readonly_fields = ('created_timestamp',)
    extra = 0

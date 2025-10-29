from django.contrib import admin

from.models import Product



class ProductAdmin(admin.ModelAdmin):

    list_display=('product_name','price','stock','category','category','modified_date','is_available')
    prepopulated_fields={'slug':('product_name',)}# single field m end m , lgana h 
admin.site.register(Product,ProductAdmin)


# Register your models here.

from django.contrib import admin
from.models import Category

class CategoryAdmin(admin.ModelAdmin):
    # this can auto the slug 
    prepopulated_fields={'slug':('category_name',)} 
    list_display=('category_name','slug') # when we enter the data in a categoryname then slug field is automatically fill
admin.site.register(Category,CategoryAdmin)


# Register your models here.

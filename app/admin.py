from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(dress)

admin.site.register(carousel_Home)



class VariationAdmin(admin.ModelAdmin):
    list_display=('product','variation_category','variation_value','is_active')
    list_editable=('is_active',)
    list_filter=('product','variation_category','variation_value',)

admin.site.register(Variation,VariationAdmin)

admin.site.register(Banner)

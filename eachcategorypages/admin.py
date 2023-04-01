from django.contrib import admin
from .models import carousel_Men,carousel_Women,carousel_Kid,Category,Product,ProImage,ReviewRating

# Register your models here.
admin.site.register(carousel_Men)
admin.site.register(carousel_Women)
admin.site.register(carousel_Kid)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('category_name',)}
    list_display=('category_name','slug')



# admin.site.register(Brand)

# class BrandAdmin(admin.ModelAdmin):
#     prepopulated_fields={'slug':('brand_name',)}
#     list_display=('brand_name','slug')


class ProImageAdmin(admin.StackedInline):
    model=ProImage 




admin.site.register(Category,CategoryAdmin)

class ProductAdmin(admin.ModelAdmin):
    list_display=('product_name','price','stock','category','modified_date','is_available')
    prepopulated_fields={'slug':('product_name',)}

    inlines=[ProImageAdmin]
 

admin.site.register(Product,ProductAdmin)

admin.site.register(ProImage)

admin.site.register(ReviewRating)


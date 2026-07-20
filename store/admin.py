from django.contrib import admin
from .models import Product, ReviewRating, Variation

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')

    prepopulated_fields = {
        'slug' : ('product_name',)
    }


class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'is_active')
    list_editable = ('is_active',)
    list_filter = ('product', 'variation_category', 'variation_value',)
    
    
    
@admin.register(ReviewRating)
class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ( 'user', 'product', 'rating', 'is_verified_purchase', 'is_approved', 'created_at' )

    list_filter = ( 'rating', 'is_verified_purchase', 'is_approved' )

    search_fields = ('user__first_name','user__last_name','product__product_name')

    list_editable = ('is_verified_purchase','is_approved')


admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)

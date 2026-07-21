from django.contrib import admin
from .models import Product, ReviewRating, Variation, VariationCategory
from .forms import VariationAdminForm


class VariationInline(admin.TabularInline):
    model = Variation
    form = VariationAdminForm
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'product_name',
        'price',
        'stock',
        'category',
        'modified_date',
        'is_available',
    )

    prepopulated_fields = {
        'slug': ('product_name',)
    }

    filter_horizontal = ('variation_categories',)

    inlines = [VariationInline]


@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = (
        'product',
        'variation_category',
        'variation_value',
        'is_active',
    )

    list_filter = (
        'product',
        'variation_category',
    )

    list_editable = ('is_active',)


@admin.register(VariationCategory)
class VariationCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(ReviewRating)
class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'product',
        'rating',
        'is_verified_purchase',
        'is_approved',
        'created_at',
    )

    list_filter = (
        'rating',
        'is_verified_purchase',
        'is_approved',
    )

    search_fields = (
        'user__first_name',
        'user__last_name',
        'product__product_name',
    )

    list_editable = (
        'is_verified_purchase',
        'is_approved',
    )
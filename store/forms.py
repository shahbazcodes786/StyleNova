from django import forms
from .models import Variation, ReviewRating, Product
from django import forms
from django.core.exceptions import ValidationError



class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewRating
        fields = ('subject', 'review')

        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Review title'
            }),

            'review': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Share your experience with this product...'
            }),
        }
        
        


class VariationAdminForm(forms.ModelForm):

    class Meta:
        model = Variation
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance and self.instance.product_id:
            self.fields["variation_category"].queryset = (
                self.instance.product.variation_categories.all()
            )
        else:
            # Naye Product ke liye sab categories dikhao
            from .models import VariationCategory
            self.fields["variation_category"].queryset = VariationCategory.objects.all()
            
            
            
class ProductAdminForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = "__all__"
        
    selling_price = forms.DecimalField(required=False,disabled=True,)

    def clean(self):
        cleaned_data = super().clean()

        discount_percentage = cleaned_data.get("discount_percentage") or 0
        discount_amount = cleaned_data.get("discount_amount") or 0


        return cleaned_data
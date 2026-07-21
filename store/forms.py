from django import forms
from .models import Variation
from django import forms
from .models import ReviewRating


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
            self.fields["variation_category"].queryset = self.fields[
                "variation_category"
            ].queryset.none()
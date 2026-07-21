from django.db import models
from category.models import Category
from django.urls import reverse
from accounts.models import Account

# Create your models here.
class Product(models.Model):
    product_name    = models.CharField(max_length=200,unique=True)
    slug            = models.SlugField(unique=True, max_length=200)
    description     = models.TextField(max_length=500,blank=True)
    price           = models.IntegerField()
    images          = models.ImageField(upload_to='photos/products')
    stock           = models.IntegerField()
    is_available    = models.BooleanField(default=True)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    variation_categories = models.ManyToManyField("VariationCategory", blank=True, related_name='products')
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)


    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
    def __str__(self):
        return self.product_name









class VariationCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = 'Variation Category'
        verbose_name_plural = 'Variation Categories'
        ordering = ['name']

    def __str__(self):
        return self.name
    
    
class Variation(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variations"
    )

    variation_category = models.ForeignKey(
    VariationCategory,
    on_delete=models.CASCADE,
    null=True,
    blank=True,
    related_name="variation_items"
)

    variation_value = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)

    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("product", "variation_category", "variation_value")

    def __str__(self):
        return f"{self.variation_category.name}: {self.variation_value}"
    
    
    
class ReviewRating(models.Model):

    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='reviews' )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews' )
    subject = models.CharField(max_length=150)
    review = models.TextField(max_length=1000)
    rating = models.PositiveSmallIntegerField(
        choices=[
            (1, '1 Star'),
            (2, '2 Stars'),
            (3, '3 Stars'),
            (4, '4 Stars'),
            (5, '5 Stars'),
        ]
    )
    is_verified_purchase = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    helpful_count = models.PositiveIntegerField(default=0)
    ip = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    class Meta:
        
        ordering = ['-created_at']
        


    def __str__(self):
        
        return f"{self.user.first_name} - {self.product.product_name}"
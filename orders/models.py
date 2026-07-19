from django.db import models
from accounts.models import Account
from store.models import Product, Variation
# Create your models here.

#in payment model we only store the information about payment
class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100, blank=True)
    payment_method = models.ForeignKey('PaymentMethod', on_delete=models.SET_NULL, null=True, blank=True)
    amount_paid = models.CharField(max_length=100)
    transaction_id = models.CharField(max_length=100)
    payment_screenshot = models.ImageField(upload_to='payment_screenshots/' )
    PAYMENT_STATUS = (
    ('pending', 'Pending'),
    ('verified', 'Verified'),
    ('rejected', 'Rejected'),
    )
    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='pending'
    )

    rejection_reason = models.TextField(
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    
    def __str__(self):
        return self.transaction_id
    
    
#in Order model we store the information about the customer
class Order(models.Model):
    ORDER_STATUS = (
    ('awaiting', 'Awaiting Confirmation'),
    ('processing', 'Processing'),
    ('packed', 'Packed'),
    ('shipped', 'Shipped'),
    ('out_for_delivery', 'Out For Delivery'),
    ('delivered', 'Delivered'),
    ('cancelled', 'Cancelled'),
)
    
    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    order_note = models.CharField(max_length=150, blank=True)
    order_total = models.FloatField()
    tax = models.FloatField()
    status = models.CharField(max_length=50, choices=ORDER_STATUS, default='awaiting')
    tracking_number = models.CharField(max_length=100, blank=True, null=True)
    ip = models.CharField(max_length=50, blank=True)
    payment_method = models.ForeignKey("PaymentMethod", on_delete=models.SET_NULL, blank=True, null=True)
    is_ordered = models.BooleanField(default=False)
    estimated_delivery = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    
    
    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'
    
    def __str__(self):
        return self.first_name
    
    
    
    
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    color = models.CharField(max_length=50, blank=True)
    size = models.CharField(max_length=50, blank=True)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True,)
    
    
    
    def __str__(self):
        return self.product.product_name
    

class PaymentMethod(models.Model):
    method = models.CharField(max_length=100, unique=True, help_text="Enter the name of the payment method (e.g., JazzCash)")
    method_logo = models.ImageField(upload_to='payment_methods/logos/', blank=True, null=True)
    display_order = models.PositiveIntegerField(default=0)
    account_name = models.CharField(max_length=150)
    account_number = models.CharField(max_length=150)
    account_qr_code = models.ImageField(upload_to='payment_methods/qr_codes/', blank=True, null=True)
    instructions = models.TextField(blank=True, help_text="Enter any specific instructions for this payment method.")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.method
    
    class Meta:
        ordering = ['display_order']